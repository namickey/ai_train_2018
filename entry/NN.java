package ai.sample;

/**
 * 最小のニューラルネットワーク（NN）
 * 入力数：1、出力数：1
 */
public class NN {

    /** 重み。初期値ランダム（0.1〜1.9） */
    private double w = (1 + Math.floor(Math.random()*19))/10;
    /** 学習率 */
    private static final double TRAIN_RATE = 0.1;
    /** 学習回数 */
    private static final int TRAIN_COUNT = 10;

    /**
     * NNの学習を行い、学習済みのNNを使用する
     * @param args args
     */
    public static void main(String[] args) {
        NN nn = new NN();
        int in = 5;
        int expected_out = 5;
        //学習回数分の学習を行う
        for(int i = 0; i < TRAIN_COUNT; i++) {
            //5を入力したら、5を出力するように覚えさせる
            nn.train(in, expected_out);
        }
        //学習済みのNNを使用する
        double out = nn.useNN(in);
        System.out.println("in:" + in + "、out:" + out);
    }

    /**
     * NNを使う
     * 入力値に重みをかける
     * @param in 入力値
     * @return 出力値
     */
    public double useNN(double in){
        return in * w;
    }

    /**
     * 学習する。
     * 期待する出力値が少ない場合、重みを増やす
     * 期待する出力値が多い場合、重みを減らす
     * 期待する出力値が正しい場合、何もしない
     * @param in 入力値
     * @param expected_out 期待する出力値
     */
    public void train(int in, int expected_out){
        if (expected_out - useNN(in) > 0) {
            w = Math.round((w + TRAIN_RATE)*10)/10.0;
        } else if (expected_out - useNN(in) < 0) {
            w = Math.round((w - TRAIN_RATE)*10)/10.0;
        }
        System.out.println("学習後の重み：" + w);
    }
}
