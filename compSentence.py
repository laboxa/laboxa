from sentence_transformers import SentenceTransformer, util

def cosineScore(text1, text2):
    # モデルのロード
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    # 文章をベクトルに変換
    embeddings1 = model.encode(text1, convert_to_tensor=True)
    embeddings2 = model.encode(text2, convert_to_tensor=True)

    # コサイン類似度の計算
    cosine_score = util.pytorch_cos_sim(embeddings1, embeddings2)[0][0]
    
    return cosine_score

if __name__ == "__main__":
    # 比較する文章
    text1 = input("文章1：")
    text2 = input("文章2：")
    
    cosine_score = cosineScore(text1, text2)
    print(f"文章1と文章2の類似度: {cosine_score}")