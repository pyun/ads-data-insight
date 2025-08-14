import streamlit as st
import requests
import os

# 页面配置
st.set_page_config(
    page_title="广告投放数据洞察",
    page_icon="📊",
    layout="wide"
)

# 主标题
st.title("📊 广告投放数据洞察")

# 创建侧边栏
with st.sidebar:
    st.header("功能菜单")
    selected_option = st.selectbox(
        "请选择功能",
        ["广告渠道数据分析"]
    )

# 主内容区域
if selected_option == "广告渠道数据分析":
    st.header("广告渠道数据分析")
    
    # 初始化session state
    if 'submitting' not in st.session_state:
        st.session_state.submitting = False
    if 'result_data' not in st.session_state:
        st.session_state.result_data = None
    
    # 工单内容输入框
    st.subheader("请输入工单内容")
    work_order_content = st.text_area(
        "",
        height=150,
        placeholder="请在此输入工单内容...",
        value = """1. 包名:com.example.social
2. 事件名称:install
3. 时间周期:20250701-20250811
4. gaid:""",

        disabled=st.session_state.submitting
    )
    
    # 文件上传
    st.subheader("请上传gaid文件")
    uploaded_file = st.file_uploader(
        "",
        type=['csv'],
        help="支持拖拽上传或点击浏览选择CSV文件",
        disabled=st.session_state.submitting
    )
    
    # 提交按钮
    if st.button("提交", type="primary", disabled=st.session_state.submitting):
        if work_order_content and uploaded_file:
            st.session_state.submitting = True
            st.session_state.result_data = None
            st.rerun()
        else:
            st.warning("请填写工单内容并上传文件后再提交")
    
    # 处理提交状态
    if st.session_state.submitting:
        with st.spinner("🤖 AI Agent正在工作中，请稍后..."):
            try:
                # 准备提交数据
                files = {"file": uploaded_file}
                data = {"user_input": work_order_content}
                
                # 提交到API
                response = requests.post(
                    "http://localhost:8000/data-query/upload-file",
                    files=files,
                    data=data
                )
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.result_data = result.get("download_url")
                else:
                    st.session_state.result_data = f"提交失败，错误代码：{response.status_code}"
                
            except Exception as e:
                st.session_state.result_data = f"提交过程中发生错误：{str(e)}"
            
            # 重置提交状态并刷新页面
            st.session_state.submitting = False
            st.rerun()
    
    # 显示结果
    if st.session_state.result_data:
        st.subheader("请查看分析结果：")
        if st.session_state.result_data.startswith("http"):
            download_url = st.session_state.result_data
            st.markdown(
                f"""
                <div style="margin-top: 10px;">
                    <a href="{download_url}" target="_blank" style="
                        display: inline-block;
                        padding: 0.5rem 1rem;
                        background-color: #0066cc;
                        color: white;
                        text-decoration: none;
                        border-radius: 0.25rem;
                        font-weight: bold;
                    ">🔗 在新窗口中打开</a>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.info(f"直接链接：{download_url}")
        else:
            st.error(st.session_state.result_data)
    