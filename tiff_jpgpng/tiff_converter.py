from PIL import Image
import os
import glob

def convert_tiff(input_folder, output_folder, output_format):
    """
    input_folder 内の TIFF/TIF を output_folder に変換保存
    output_format: "JPEG" または "PNG"
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 対応拡張子（大小文字対応）
    extensions = ["*.tif", "*.tiff", "*.TIF", "*.TIFF"]
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(input_folder, ext)))

    if not files:
        print(f"{input_folder} に変換対象のTIFFがありません。")
        return

    for file in files:
        try:
            with Image.open(file) as img:
                # JPEG出力時にRGBAやPモードをRGBに変換
                if output_format == "JPEG" and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                    # 透明情報（アルファ）は消えて背景は結合される（PNG の場合はこの変換はしないので透明を保持できる）。
                filename = os.path.splitext(os.path.basename(file))[0]
                out_file = os.path.join(
                    output_folder,
                    filename + (".jpg" if output_format == "JPEG" else ".png")
                )

                # 高品質設定
                if output_format == "JPEG":
                    img.save(out_file, output_format, quality=95)
                else:
                    img.save(out_file, output_format)

                print(f"変換完了: {file} → {out_file}")
        except Exception as e:
            print(f"変換失敗: {file} → {e}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    to_jpeg_dir = os.path.join(base_dir, "toJPEG")
    to_png_dir = os.path.join(base_dir, "toPNG")
    output_dir = os.path.join(base_dir, "output")

    print("=== TIFF → JPEG 変換開始 ===")
    convert_tiff(to_jpeg_dir, output_dir, "JPEG")

    print("\n=== TIFF → PNG 変換開始 ===")
    convert_tiff(to_png_dir, output_dir, "PNG")

    print("\n全変換処理が完了しました。")
