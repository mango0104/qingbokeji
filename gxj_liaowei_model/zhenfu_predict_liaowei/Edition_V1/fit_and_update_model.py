import joblib
from apscheduler.schedulers.blocking import BlockingScheduler
import numpy as np
from sklearn.linear_model import LinearRegression
import subprocess
import os

def fit_and_update_model():
    try:
        # 线性回归的横纵坐标
        X = np.array([24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]).reshape(-1, 1)
        y = np.array([2.94, 3.029, 3.118, 3.207, 3.296, 3.385, 3.474, 3.562, 3.651, 3.740, 3.829, 3.918])

        # 初始化模型
        model = LinearRegression()

        # 训练模型
        model.fit(X, y)

        # 保存模型到本地特定路径
        local_save_path = 'model.pkl'
        joblib.dump(model, local_save_path)
        print(f"模型已保存到本地 {local_save_path}")

        # 设置 GitHub 仓库路径
        github_repo = 'git clone ssh://git@111.15.165.82:2200/gitlab-instance-b03aeb89/jhzn_gxj_predict.git'
        repo_folder = 'jhzn_gxj_predict'

        # 克隆仓库（如果不存在）
        if not os.path.exists(repo_folder):
            subprocess.run(['git', 'clone', github_repo])

        # 将模型文件复制到仓库目录
        import shutil
        shutil.copy(local_save_path, os.path.join(repo_folder, local_save_path))

        # 进入仓库目录
        os.chdir(repo_folder)

        # 添加文件到暂存区
        subprocess.run(['git', 'add', local_save_path])

        # 提交更改
        subprocess.run(['git', 'commit', '-m', 'Update model.pkl'])

        # 推送更改到 GitHub
        subprocess.run(['git', 'push', 'origin', 'main'])

        print(f"模型已成功推送到 {github_repo}")

    except Exception as e:
        print(f"训练、保存或推送模型时出错: {e}")


# 运行函数
fit_and_update_model()