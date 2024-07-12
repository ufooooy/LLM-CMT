package dataset1123;

import java.security.SecureRandom;

public class SetSeedMisuseExample {

    public static void main(String[] args) {
        // 创建SecureRandom实例
        SecureRandom secureRandom = new SecureRandom();

        // 设置固定的种子（错误用法）
        secureRandom.setSeed(123456L);

        // 生成伪随机数
        int randomValue = secureRandom.nextInt(100);

        System.out.println("Generated random value: " + randomValue);
    }
}
