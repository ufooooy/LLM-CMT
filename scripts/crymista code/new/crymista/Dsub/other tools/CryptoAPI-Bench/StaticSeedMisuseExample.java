package dataset1123;

import java.security.SecureRandom;

public class StaticSeedMisuseExample {

    private static final long STATIC_SEED = 123456L;

    public static void main(String[] args) {
        // 创建SecureRandom实例并设置固定的种子（错误用法）
        SecureRandom secureRandom = new SecureRandom();
        secureRandom.setSeed(STATIC_SEED);

        // 生成伪随机数
        int randomValue = secureRandom.nextInt(100);

        System.out.println("Generated random value: " + randomValue);
    }
}
