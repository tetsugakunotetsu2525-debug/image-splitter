import streamlit as st
from PIL import Image
import zipfile
from io import BytesIO

st.set_page_config(page_title="画像16:9分割ツール", layout="wide")

st.title("📸 画像16:9分割ツール")
st.markdown("任意の画像を16:9にトリミングして、中央から4分割します")

uploaded_file = st.file_uploader("画像をアップロード", type=['png', 'jpg', 'jpeg', 'bmp', 'gif'])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    original_width, original_height = img.size
    
    st.write(f"**元のサイズ:** {original_width} × {original_height}")
    
    target_ratio = 16 / 9
    current_ratio = original_width / original_height
    
    if current_ratio > target_ratio:
        new_width = int(original_height * target_ratio)
        left = (original_width - new_width) // 2
        right = left + new_width
        img_cropped = img.crop((left, 0, right, original_height))
    else:
        new_height = int(original_width / target_ratio)
        top = (original_height - new_height) // 2
        bottom = top + new_height
        img_cropped = img.crop((0, top, original_width, bottom))
    
    crop_width, crop_height = img_cropped.size
    st.write(f"**16:9トリミング後:** {crop_width} × {crop_height}")
    
    center_x = crop_width // 2
    center_y = crop_height // 2
    
    top_left = img_cropped.crop((0, 0, center_x, center_y))
    top_right = img_cropped.crop((center_x, 0, crop_width, center_y))
    bottom_left = img_cropped.crop((0, center_y, center_x, crop_height))
    bottom_right = img_cropped.crop((center_x, center_y, crop_width, crop_height))
    
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
    
    st.subheader("ダウンロード")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        buf1 = BytesIO()
        top_left.save(buf1, format='PNG')
        buf1.seek(0)
        st.download_button("1.png", buf1.getvalue(), "1.png", "image/png", key="1")
    
    with col2:
        buf2 = BytesIO()
        top_right.save(buf2, format='PNG')
        buf2.seek(0)
        st.download_button("2.png", buf2.getvalue(), "2.png", "image/png", key="2")
    
    with col3:
        buf3 = BytesIO()
        bottom_left.save(buf3, format='PNG')
        buf3.seek(0)
        st.download_button("3.png", buf3.getvalue(), "3.png", "image/png", key="3")
    
    with col4:
        buf4 = BytesIO()
        bottom_right.save(buf4, format='PNG')
        buf4.seek(0)
        st.download_button("4.png", buf4.getvalue(), "4.png", "image/png", key="4")
    
    st.write("---")
    
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
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
        
        buf_crop = BytesIO()
        img_cropped.save(buf_crop, format='PNG')
        zipf.writestr('cropped_16_9.png', buf_crop.getvalue())
    
    zip_buffer.seek(0)
    st.download_button(
        label="📦 全てZIPでダウンロード",
        data=zip_buffer.getvalue(),
        file_name="divided_images.zip",
        mime="application/zip",
        key="zip"
    )

else:
    st.info("👆 上から画像をアップロードして開始してください")
