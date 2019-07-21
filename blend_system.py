import pandas as pd
import numpy as np
import random

df_blend = pd.read_csv("./documents/indesign/cofee_blend.csv", encoding = "utf_8")
df_taste = pd.read_csv("./documents/indesign/blend_feature.csv", encoding = "utf_8")
df_user = pd.read_csv("./documents/indesign/user_info.csv", encoding = "utf_8")



morning_flag = 0
use_counts = 1

#初めての使用時は、黄金比と呼ばれるブレンドをおすすめ
if use_counts ==0:
    recomend_base_beans={"name":"colo", "ratio":4}

#night phase　　morning_phaseに確定したブレンド配合を渡す
#ベースが決まる。使えるブレンドを絞り込み
#おすすめを見つけるための処理　出力：要素6つのリスト。前からブラジルの割合、コロンビアの割合,,,って感じで渡す。

base_name = "colo"
base_ratio = 4

base_beans={}  #ベースの豆情報を格納するdict。name:豆の種類(bra, colo, gua, man, moch, kili), ratio:豆の割合。1セットのブレンドのratio合計が10になる
base_beans["name"] = base_name
base_beans["ratio"] = base_ratio

df_candidate_blend = df_blend[df_blend[base_beans["name"]] == base_beans["ratio"]]
print(df_candidate_blend)

if use_counts ==0:
    recomend_list=["colo4bra3moch2man1", "colo4bra3moch3"]  #黄金比
    if base_beans == {"name":"colo", "ratio":4}:
        str_recomend_blend = random.choice(recomend_list)  #2つの黄金比のどちらかをランダム選択
        print(str_recomend_blend)
    else:
        str_recomend_blend = df_candidate_blend.iat[random.randint(0, len(df_candidate_blend)-1), 0]  #ユーザがおすすめに従わなかった場合は、ランダム
        print(str_recomend_blend)
else:
    df_user_favorite = df_user[df_user['star'] == 3]
    df_user_hated = df_user[df_user['star'] == 1]
    
    if(len(df_user_favorite) != 0):
        user_blend_taste = create_blend_taste_data(df_user_favorite['blend'].values.tolist())  #味のスコア化をしたデータを持ってくる
        np.sum(user_blend_taste, axis=0)
        #平均取る
        #averaging_blend_taste =
        print(user_blend_taste)
        
        candidate_blend_taste = create_blend_taste_data(df_candidate_blend['blend'].values.tolist())
        print(candidate_blend_taste)
        
        
        
        
#         similarities = get_correlation_coefficents(candidate_blend_taste, averaging_blend_taste)

#         print('Similarities: {}'.format(similarities))
#         # Similarities: [(186, 1.0), (269, 1.0), (381, 1.0), ...

#         print('scores[186]:\n{}'.format(scores[186]))


def create_blend_taste_data(blend_list):
    candidate_blend_taste = pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
#     print(df_blend)
    for blend_name in blend_list:
        df_blend_taste = df_taste[df_taste['blend'] == blend_name]  
        candidate_blend_taste = pd.concat([candidate_blend_taste, df_blend_taste])     
    
    df_score = candidate_blend_taste.drop("blend", axis=1).values  #ndarrayを返す
    
    return df_score



#引数二つに被りがあった時が気になる。類似度1になるに決まってる
def get_correlation_coefficents(scores, target_user_index):
    similarities = []
    target = scores[target_user_index]
    
    for i, score in enumerate(scores):        
        similarity = np.corrcoef(target[indices], score[indices])[0, 1]
        if np.isnan(similarity):
            continue
    
        similarities.append((i, similarity))
    
    return sorted(similarities, key=lambda s: s[1], reverse=True)  #☆3やったらこれで、☆1やったら逆順ソート
    
    
    
    
#morning phase　　night_phaseにおすすめベースを渡す。いや、おすすめベースを格納しとく用のテキストファイルがいるのか。
#決定したブレンドで豆を排出
#お気に入りのフィードバックが☆として返ってくるので、それを保存
#今日のブレンドデータをuser_info.csvに追記

#可視化のために、user_info.csvからGUI側に必要情報を提示。渡すときはdictで割合を渡す

#次の夜のおすすめを選択する

use_counts+=1


