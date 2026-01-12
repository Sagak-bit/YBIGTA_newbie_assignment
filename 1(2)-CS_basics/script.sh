
# anaconda(또는 miniconda)가 존재하지 않을 경우 설치해주세요!
if ! command -v conda >/dev/null 2>&1; then
    if [[ ! -x "$HOME/miniconda3/bin/conda" ]]; then
        wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda3.sh
        bash miniconda3.sh -b -p "$HOME/miniconda3"
        rm -f miniconda3.sh
    fi
    export PATH="$HOME/miniconda3/bin:$PATH"
fi

export CONDA_PLUGINS_AUTO_ACCEPT_TOS=yes

# Conda 환경 생성 및 활성화
source "$(conda info --base)/etc/profile.d/conda.sh"
if ! conda env list | grep -qE '^myenv\s'; then
    conda create -n myenv -y -q python=3.11 pip
fi

conda activate myenv

## 건드리지 마세요! ##
python_env=$(python -c "import sys; print(sys.prefix)")
if [[ "$python_env" == *"/envs/myenv"* ]]; then
    echo "[INFO] 가상환경 활성화: 성공"
else
    echo "[INFO] 가상환경 활성화: 실패"
    exit 1 
fi

# 필요한 패키지 설치

python -m pip install -q --upgrade pip
python -m pip install -q mypy

# Submission 폴더 파일 실행
cd submission || { echo "[INFO] submission 디렉토리로 이동 실패"; exit 1; }

mkdir -p ../output
compgen -G "*.py" > /dev/null || { echo "[ERROR] submission에 .py 파일이 없음"; exit 1; }

for file in *.py; do
    prob="${file##*_}"
    prob="${prob%.py}"

    in_path="../input/${prob}_input"
    out_path="../output/${prob}_output"

    [[ -f "$in_path" ]] || { echo "[ERROR] 입력 파일 없음: $in_path"; exit 1; }
    python "$file" < "$in_path" > "$out_path" || { echo "[ERROR] 실행 실패: $file"; exit 1; }
done


# mypy 테스트 실행 및 mypy_log.txt 저장
cd ..
mypy submission/*.py > mypy_log.txt 2>&1 || exit 1

# mypy 캐시 정리
rm -rf .mypy_cache

# conda.yml 파일 생성
conda env export -n myenv --no-builds > conda.yml

# 가상환경 비활성화
conda deactivate