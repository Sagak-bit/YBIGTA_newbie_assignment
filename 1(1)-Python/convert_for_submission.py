import sys
import os 

PATH_1 = "./1-graph-traversal" 
PATH_2 = "./2-stack-queue-deque"
PATH_3 = "./3-divide-and-conquer-multiplication"
PATH_4 = "./4-trie"
PATH_5 = "./5-segment-tree"

ROOT_PATH = {
    "1260": PATH_1,
    "2164": PATH_2,
    "11866": PATH_2,
    "1629": PATH_3,
    "10830": PATH_3,
    "3080": PATH_4,
    "5670": PATH_4,
    "2243": PATH_5,
    "3653": PATH_5,
    "17408": PATH_5
}

PATH_SUB = "./submission" 

def integrate_file(n: str) -> None:
    n = str(n).replace(".py", "")
    
    os.makedirs(PATH_SUB, exist_ok=True)

    target_path = f"{ROOT_PATH[n]}/{n}.py"
    lib_path = f"{ROOT_PATH[n]}/lib.py"
    
    num_code = "".join(filter(lambda x: "from lib import" not in x, open(target_path, encoding='utf-8').readlines()))
    
    lib_code = open(lib_path, encoding='utf-8').read()
    
    integrated_code = lib_code + "\n\n\n" + num_code

    if n == "1629": 
        integrated_code = num_code 
        
    folder_num = ROOT_PATH[n][2]
    
    output_path = f"{PATH_SUB}/{folder_num}_{n}.py"
    open(output_path, 'w', encoding='utf-8').write(integrated_code)
    
    print(f"생성 완료: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) == 2: 
        file_id = sys.argv[1]
        integrate_file(file_id)    
    else: 
        for file in ROOT_PATH:
            integrate_file(file)