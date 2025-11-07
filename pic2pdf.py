from pathlib import Path
from PIL import Image
from dataclasses import dataclass


@dataclass
class Pic2PDF:
    base_dir: Path  # 待处理的图片所在目录
    out_dir: Path  # 转换后的PDF文件保存的位置，未指定则与图片在同一目录
    width: int | None = None  # 转换后图片的宽度
    dpi: int | None = None  # 转换后图片的dpi

    @staticmethod
    def adjust_size(pic_path: Path, target_width: int, target_dpi: int) -> None:
        """
        调整图片的尺寸和dpi.
        参数:
        pic_path: 图片文件的路径.
        target_width: 目标宽度.
        target_dpi: 目标dpi(分辨率).
        """
        # 打开图片
        im = Image.open(pic_path)
        # 获取图片当前的宽度和高度
        width, high = im.size
        dpi = im.info.get("dpi")
        if width == target_width and dpi == target_dpi:
            return
        # 调整图片尺寸, 保持长宽比, 并保存
        im.resize(size=(target_width, int(target_width / width * high))).save(
            pic_path, dpi=(target_dpi, target_dpi)
        )

    def get_size(self, img_dir: Path) -> tuple[int, int]:
        """
        获取图片文件夹中图片的最小宽度和最大dpi.
        参数:
        - img_dir: 字符串, 指定的图片文件夹路径.
        """
        # 如果已有宽度和dpi值, 则直接返回
        if self.width and self.dpi:
            return self.width, self.dpi
        # 初始化目标宽度和dpi
        target_width: int = int(1e7)
        target_dpi: int = 0
        # 遍历文件夹中的所有文件
        for file in img_dir.iterdir():
            # 仅处理JPG和PNG文件
            if not file.name.endswith((".jpg", ".png")):
                continue
            img = Image.open(file)
            # 更新目标宽度为当前处理图片中最小的宽度
            if not self.width:
                target_width = min(target_width, img.size[0])
            # 更新目标dpi为当前处理图片中最大的dpi
            if not self.dpi:
                target_dpi = max(target_dpi, img.info.get("dpi", 0))

        # 如果已有宽度和/或dpi值, 使用它们；否则使用扫描图片得到的值
        width = self.width if self.width else target_width
        dpi = self.dpi if self.dpi else target_dpi
        return width, dpi

    def pic2pdf(self, img_dir: Path, del_old: bool) -> None:
        """
        将指定文件夹中的所有图片转换为一个PDF文件.
        参数:
        - img_dir: 图片所在的文件夹路径.
        - out_dir: PDF保存的路径.
        - del_old: 转换完成后是否删除原始图片, 默认为True.
        """
        target_width, target_dpi = self.get_size(img_dir)
        file_list: list[Path] = []
        for file in img_dir.iterdir():
            if file.name.endswith((".jpg", "png")):
                Pic2PDF.adjust_size(file, target_width, target_dpi)
                file_list.append(file)
        if len(file_list) == 0:
            print(f"{img_dir}: no images")
            return
        # 准备图片列表, 用于生成PDF
        image_list = [Image.open(image).convert("RGB") for image in file_list]
        # 生成PDF
        image_list[0].save(
            self.out_dir / f"{img_dir.name}.pdf",
            "PDF",
            resolution=100.0,
            save_all=True,
            append_images=image_list[1:],
        )
        # 如果需要, 删除转换前的图片
        if del_old:
            for file in file_list:
                file.unlink()
        # 如果图片文件夹为空, 删除该文件夹
        if not img_dir.iterdir():
            img_dir.rmdir()
        print(f"{img_dir} to pdf complete")

    def main(self, del_old: bool = True) -> None:
        """
        检测base_dir下所有子目录, 并对每个包含图片的目录执行pic2pdf方法.
        """
        self.pic2pdf(
            self.base_dir,
            del_old,
        )
        for root, dirs, _ in self.base_dir.walk():
            for dir in dirs:
                self.pic2pdf(root / dir, del_old)


if __name__ == "__main__":
    base_dir = Path().cwd()
    out_dir = Path().cwd()
    toPDF = Pic2PDF(base_dir=base_dir, out_dir=out_dir)
    toPDF.main(del_old=False)
    # for p in Path("your path").iterdir():
    #     Pic2PDF.adjust_size(Path(p), 2500, 96)
