import pandas as pd
import numpy as np
import random

df_blend = pd.read_csv("./documents/indesign/cofee_blend.csv", encoding = "utf_8")
df_taste = pd.read_csv("./documents/indesign/blend_feature.csv", encoding = "utf_8")




morning_flag = 0
use_counts = 1

#初めての使用時は、黄金比と呼ばれるブレンドをおすすめ
if use_counts ==0:
    recomend_base_beans={"name":"colo", "ratio":4}


# base_name = "colo"
# base_ratio = 4



def decide_blend_ratio(user_data, candidate_data, star):
    '''
    input:
    '''
    user_blend_list = user_data['blend'].values.tolist()
    if len(user_blend_list) <= 2:  #サンプルが少ない状況だと類似度が1になりやすく、同じ配合ばかりが繰り返し推薦される可能性があるので、同じものは候補から取り除く
        for blend_name in user_blend_list:
            candidate_data = candidate_data[candidate_data['blend'] != blend_name]
            
    user_blend_taste = create_blend_taste_data(user_blend_list)  #味のスコア化をしたデータを持ってくる
    averaging_blend_taste = np.sum(user_blend_taste, axis=0) / len(user_blend_taste)   #平均取る

    candidate_blend_list = candidate_data['blend'].values.tolist()
    candidate_blend_taste = create_blend_taste_data(candidate_blend_list)

    similarities = get_correlation_coefficents(candidate_blend_taste, averaging_blend_taste, star)   #類似度を計算
    print(similarities)
    selected_blend_name = candidate_blend_list[similarities[0][0]]
    
    return selected_blend_name



def create_blend_taste_data(blend_list):
    candidate_blend_taste = pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
    for blend_name in blend_list:
        df_blend_taste = df_taste[df_taste['blend'] == blend_name]  
        candidate_blend_taste = pd.concat([candidate_blend_taste, df_blend_taste])     
    
    df_score = candidate_blend_taste.drop("blend", axis=1).values  #ndarrayを返す
    
    return df_score



#引数二つに被りがあった時が気になる。類似度1になるに決まってる
def get_correlation_coefficents(candidate_scores, user_score, star):
    similarities = []
    
    for i, score in enumerate(candidate_scores):
        similarity = np.corrcoef(user_score, score)[0, 1]
        if np.isnan(similarity):
            continue
        similarities.append((i, similarity))
    
    if star == 3:  #☆3やったらこれで、☆1やったら逆順ソート
        return sorted(similarities, key=lambda s: s[1], reverse=True)
    elif star == 1:
        return sorted(similarities, key=lambda s: s[1], reverse=False)
        
        

#night phase　　機構側とmorning_phaseに　確定したブレンド配合を渡す
def night_phase(base_name = colo, base_ratio = 4):  ##初めての使用時は、黄金比と呼ばれるブレンドをおすすめ 
    '''
    引数：ベースの豆の名前と割合　(GUIからもらう)
    おすすめを見つけるための処理　
    出力：要素6つのリスト。前からブラジルの割合、コロンビアの割合,,,って感じで渡す。
    '''
    base_beans={}  #ベースの豆情報を格納するdict。name:豆の種類(bra, colo, gua, man, moch, kili), ratio:豆の割合。1セットのブレンドのratio合計が10になる
    base_beans["name"] = base_name
    base_beans["ratio"] = base_ratio
    
    df_user = pd.read_csv("./documents/indesign/user_info.csv", encoding = "utf_8")

    df_candidate_blend = df_blend[df_blend[base_beans["name"]] == base_beans["ratio"]]　　　#ベースに合わせて使えるブレンドを絞り込み
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
            str_recomend_blend = decide_blend_ratio(df_user_favorite, df_candidate_blend, 3)
            print(str_recomend_blend)
        elif(len(df_user_hated) != 0):
            str_recomend_blend = decide_blend_ratio(df_user_hated, df_candidate_blend, 1)
            print(str_recomend_blend)
        else:
            str_recomend_blend = df_candidate_blend.sample().iat[0, 0]   #好きも嫌いもないということなので、次はランダムに選ぶ
            print(str_recomend_blend)


    df_selected_blend = df_blend[df_blend['blend'] == str_recomend_blend]
    selected_blend_ratio = df_selected_blend.drop("blend", axis=1).values.tolist()
    print(selected_blend_ratio[0])
    
    return selected_blend_ratio[0], str_recomend_blend        