import streamlit as st
from PIL import Image
import io
import zipfile
from io import BytesIO

st.set_page_config(page_title="画像16:9分割ツール", layout="wide")

st.title("📸 画像16:9分割ツール")
st.markdown("任意の画像を16:9にトリミングして、中央から4分割します")

# ファイルアップロード
uploaded_file = st.file_uploader("画像をアップロード", type=['png', 'jpg', 'jpeg', 'bmp', 'gif'])

if uploaded_file is not None:
    # 画像を開く
    img = Image.open(uploaded_file)
    original_width, original_height = img.size
    
    st.write(f"**元のサイズ:** {original_width} × {original_height}")
    
    # 16:9にトリミング
    target_ratio = 16 / 9
    current_ratio = original_width / original_height
    
    if current_ratio > target_ratio:
        # 幅が広すぎる場合、幅を調整
        new_width = int(original_height * target_ratio)
        left = (original_width - new_width) // 2
        right = left + new_width
        img_cropped = img.crop((left, 0, right, original_height))
    else:
        # 高さが高すぎる場合、高さを調整
        new_height = int(original_width / target_ratio)
        top = (original_height - new_height) // 2
        bottom = top + new_height
        img_cropped = img.crop((0, top, original_width, bottom))
    
    crop_width, crop_height = img_cropped.size
    st.write(f"**16:9トリミング後:** {crop_width} × {crop_height}")
    
    # 中央から4分割
    center_x = crop_width // 2
    center_y = crop_height // 2
    
    # 4つのセクションに分割
    top_left = img_cropped.crop((0, 0, center_x, center_y))
    top_right = img_cropped.crop((center_x, 0, crop_width, center_y))
    bottom_left = img_cropped.crop((0, center_y, center_x, crop_height))
    bottom_right = img_cropped.crop((center_x, center_y, crop_width, crop_height))
    
    # 分割結果を表示
    st.subheader("分割結果")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**1. 左上**")
        st.image(top_left, use_column_width=True)
    
    with col2:
        st.write("**2. 右上**")
        st.image(top_right, use_column_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.write("**3. 左下**")
        st.image(bottom_left, use_column_width=True)
    
    with col4:
        st.write("**4. 右下**")
        st.image(bottom_right, use_column_width=True)
    
    # ダウンロード機能
    st.subheader("ダウンロード")
    
    # 個別ダウンロード
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        buf = BytesIO()
        top_left.save(buf, format='PNG')
        st.download_button("1.png", buf.getvalue(), "1.png", "image/png")
    
    with col2:
        buf = BytesIO()
        top_right.save(buf, format='PNG')
        st.download_button("2.png", buf.getvalue(), "2.png", "image/png")
    
    with col3:
        buf = BytesIO()
        bottom_left.save(buf, format='PNG')
        st.download_button("3.png", buf.getvalue(), "3.png", "image/png")
    
    with col4:
        buf = BytesIO()
        bottom_right.save(buf, format='PNG')
        st.download_button("4.png", buf.getvalue(), "4.png", "image/png")
    
    # ZIPでまとめてダウンロード
    st.write("---")
    st.write("**すべてをZIPでダウンロード**")
    
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        # 分割画像
        buf1 = BytesIO()
        top_left.save(buf1, format='PNG')
        zipf.writestr('1.png', buf1.getvalue())
        
        buf2 = BytesIO()
        top_right.save(buf2, format='PNG')
        zipf.writestr('2.png', buf2.getvalue())
        
        buf3 = BytesIO()
        bottom_left.save(buf3, format='PNG')
        zipf.writestr('3.png', buf3.getvalue())
        
        buf4 = BytesIO()
        bottom_right.save(buf4, format='PNG')
        zipf.writestr('4.png', buf4.getvalue())
        
        # 全体画像
        buf_crop = BytesIO()
        img_cropped.save(buf_crop, format='PNG')
        zipf.writestr('cropped_16_9.png', buf_crop.getvalue())
    
    zip_buffer.seek(0)
    st.download_button(
        label="📦 divided_images.zip",
        data=zip_buffer.getvalue(),
        file_name="divided_images.zip",
        mime="application/zip"
    )
else:
    st.info("👆 上から画像をアップロードして開始してください")
