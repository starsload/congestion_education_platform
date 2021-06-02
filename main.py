import streamlit as st
import pandas as pd
import time
from PIL import Image
import matplotlib.pyplot as plt

cur_time = 1

#定义装饰器，加载数据
@st.cache
def load_data(path):
    file = open(path)
    data = file.readlines()
    para_1 = []
    para_2 = []
    for num in data:
        para_1.append(float(num.split('\t')[0]))
        para_2.append(float(num.split('\t')[1]))
    return list(para_1),list(para_2)

#动态绘制折线图,index是时间，data是拥塞窗口
def draw(index,data,path):
    # 取得数据
    Al_len = float(index[len(index) - 1])

    print(Al_len)

    data_counter = len(index)#数据量大小
    slit = data_counter//100#分段
    name = path.split('_')[0]

    # 加到侧边栏
    Al_cur = st.sidebar.slider(
        name+'调整：', 1.0, Al_len, 1.0, 0.01
    )

    # 绘制动态折线图
    i = 0
    pl = st.empty()
    while index[i] < Al_cur:
        i += slit
        chart_data = pd.DataFrame(
           data=data[0:i], index=index[0:i], columns=[name])
        pl.line_chart(chart_data)
        time.sleep(0.1)
        # while st.button(name+'仿真开始/暂停'):
        #     i += slit
        #     chart_data = pd.DataFrame(
        #         data=data[0:i], index=index[0:i], columns=[name])
        #     pl.line_chart(chart_data)
        #     time.sleep(0.1)

def main():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.title('TCP拥塞控制算法展示平台')

    st.subheader("算法对比表:")
    st.image("compare.png")

    # 显示拓扑
    st.subheader('拓扑网络图:')
    net = Image.open('bupt_c.png')
    st.image(net)

    # 选择框
    st.subheader('请选择你要模拟的网络配置（数据传输率，时延）：')
    option = st.selectbox(
        '',
        ['5Mbps\t10ms',
         '5Mbps\t100ms',
         '100Mbps\t10ms',
         '100Mbps\t100ms',
         '500Mbps\t10ms',
         '500Mbps\t100ms'])

    # 吞吐量比较图
    st.subheader('吞吐量比较图：')
    comparation = option.split('\t')[0]+'_'+option.split('\t')[1]
    st.image(comparation+'.jpg')

    #读取数据
    NewReno_index,NewReno_data = load_data('NewReno_data.txt')
    Westwood_index,Westwood_data = load_data('Westwood_data.txt')
    Veno_index,Veno_data = load_data('Veno_data.txt')
    BIC_index,BIC_data = load_data('BIC_data.txt')
    CUBIC_index,CUBIC_data = load_data('CUBIC_data.txt')

    #绘制对比折线图
    st.subheader('TCP拥塞控制算法拥塞窗口对比图：')
    plt.plot(NewReno_index,NewReno_data,color = 'green',label = 'NewReno')
    plt.plot(Westwood_index,Westwood_data,color = 'red',label = 'Westwood')
    plt.plot(Veno_index,Veno_data,color = 'purple',label = 'Veno')
    plt.plot(BIC_index,BIC_data,color = 'blue',label = 'BIC')
    plt.plot(CUBIC_index,CUBIC_data,color = 'brown',label = 'CUBIC')
    plt.legend()#显示图例
    plt.xlabel('time/s',fontsize = 20)
    plt.ylabel('Cwnd/Bytes',fontsize = 20)
    plt.gca().margins(x=0)
    plt.gcf().canvas.draw()
    tl = plt.gca().get_xticklabels()
    # maxsize = max([t.get_window_extent().width for t in tl])
    maxsize = 30
    m = 0.2  # inch margin
    s = maxsize / plt.gcf().dpi * 50 + 2 * m
    margin = m / plt.gcf().get_size_inches()[0]
    plt.gcf().subplots_adjust(left=margin, right=1. - margin)
    plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])
    st.pyplot()


    #算法仿真执行
    al_option = st.sidebar.selectbox('请选择要进行仿真演示的TCP拥塞控制算法：',
                                     ['NewReno',
                                      'Westwood',
                                      'Veno',
                                      'BIC',
                                      'CUBIC'])
    if al_option == 'NewReno':
        st.subheader('NewReno:')
        draw(NewReno_index,NewReno_data,'NewReno_data.txt')
    elif al_option == 'Westwood':
        st.subheader('Westwood:')
        draw(Westwood_index, Westwood_data, 'Westwood_data.txt')
    elif al_option == 'Veno':
        st.subheader('Veno:')
        draw(Veno_index, Veno_data, 'Veno_data.txt')
    elif al_option == 'BIC':
        st.subheader('BIC:')
        draw(BIC_index, BIC_data, 'BIC_data.txt')
    else :
        st.subheader('CUBIC:')
        draw(CUBIC_index, CUBIC_data, 'CUBIC_data.txt')
    st.title("\n")
    st.title("\n")
    st.title("\n")

    connection = st.checkbox("联系我")
    if connection:
        st.write("开发者：陈立伟")
        st.write("邮箱：641745039@qq.com")


if __name__ == '__main__':
    main()
