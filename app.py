#必要なライブラリをインポート
import streamlit as st
import pandas as pd
import plotly.express as px
import math
import matplotlib.pyplot as plt
import pyperclip
import numpy as np

#タイトル
st.title("🎉🎉週刊TODA🎉🎉")

#csvアップローダーをサイドバーに設置
upload_file = st.sidebar.file_uploader("ファイルアップロード", type='csv') 

#アップロードしたcsvをpre_dfに代入し、最終行をカットしてdfへ代入
pre_df = pd.read_csv(upload_file)
df = pre_df[:-1]

#小テストの受講状況「状態」をdf_test_stateに代入
df_test_state = df[['状態']]

# ---受験率を算出---

#test_stateをカウント→cours_studentsへ格納（cours_students = コースの学生数）
cours_students=df_test_state.count()
#test_stateのうち、「-」をカウント（テストを受けていない数をカウント）
not_taken=df_test_state[df_test_state['状態']=='-'].count()
#test_stateのうち、「終了」をカウント（テストを受けた数をカウント）
ok_taken=df_test_state[df_test_state['状態']=='終了'].count()
#コースの学生数＝テスト済み+テスト未
all_taken = not_taken + ok_taken
#受験率＝テストを受けた数/コースの学生数
test_rate = ok_taken/all_taken
#受験率を出力（%で表示するため、100を乗算して文字列へ変換）
test_rate2 = str(math.floor(test_rate * 100)) + "%"

test_rate3=float(test_rate)
st.markdown(f'受験率は{test_rate2}です、皆さん頑張りましょう！')
if test_rate3 == 1.0:
    st.markdown('全員受験してますね、素晴らしいです。')
elif test_rate3 > 0.5:
    st.markdown('半分以上の学生が受験していますね、良い感じです。')
else:
    st.markdown('まずは受験しまょう。')


#---平均点の出力---

#object型であるため、int型に変換
df2 = df[df['状態']=='終了']
df2['評点/10.00'] = df2['評点/10.00'].astype(float).astype(int)
#df2の合計を人数で割り算して平均点を算出
average_score=int(df2['評点/10.00'].sum() / len(df2))
st.markdown(f'小テストを受験した人の平均点は{average_score}点です。')
if average_score == 10:
    st.markdown('頑張ってますね。')
elif average_score > 6:
    st.markdown('もう一息です。')
else:
    st.markdown('全体的に苦戦しているようです。')

#グラフを２カラムで表示させる
col1, col2 = st.columns(2)

#col1に受験状況のpie_chartを表示
with col1:
   #---受験状況をグラフ化---
    st.markdown('👇受験状況👇')
    labels = ["not_taken", "ok_taken"]
    sizes = [int(not_taken),int(ok_taken)]
    fig, ax = plt.subplots(figsize=(5,5))
    ax.pie(sizes, labels=labels, autopct="%1.1f%%")
    ax.axis("equal")
    st.pyplot(fig)

#col2に小テストの得点分布をhistで表示
with col2:
  #---ヒストグラムを表示---
    st.markdown('👇得点分布👇')
    arr = np.random.normal(1, 1, size=100)
    fig, ax = plt.subplots()
    plt.xlabel('Score distribution')
    plt.ylabel('Number of peaople')
    ax.hist(df2['評点/10.00'], bins=20)
    st.pyplot(fig)

#dfから「評点」の列を抽出
df_score = df2['評点/10.00'] 

#最高点
df_score.max()
max_score = df_score.max()
min_score = df_score.min()
st.markdown(f'最高点は{max_score}、最低点は{min_score}でした。')
