#include <iostream>
#include <vector>

using namespace std;

vector<vector<int>> result;

void cut(vector<int> a, int point, vector<vector<int>> all, vector<int> sum){
    if(!result.empty()){
        return;
    }

    // 全部分完
    if(point == a.size()){
        // 检查是否满足
        if(sum[0] + sum[1] > sum[2] && sum[2] + sum[1] > sum[0] && sum[0] + sum[2] > sum[1]){
            result = all;
        }
        return ;
    }

    for(int i=0; i<3; i++) {
        // 分给第i人
        all[i].push_back(a[point]);
        sum[i] += a[point];

        cut(a, point+1, all, sum);

        sum[i] -= a[point];
        all[i].pop_back();
    }
}

int main() {
    int n;
    scanf("%d", &n);
    vector<int> a;
    for(int i=0; i<n; i++){
        int tmp;
        scanf("%d", &tmp);
        a.push_back(tmp);
    }

    vector<int> sum(3, 0);

    vector<int> a1;
    vector<int> a2;
    vector<int> a3;
    vector<vector<int>> all;
    all.push_back(a1);
    all.push_back(a2);
    all.push_back(a3);

    // 从第0块开始分
    cut(a, 0, all, sum);
    if(result.empty()){
        cout << "Internationale!";
    }

    vector<string> out(a.size(),"");
    vector<string> name = {"B", "Y", "Z"};

    for(int i=0; i<3; i++){
        for(int j=0; j<result[i].size(); j++){
            for(int k=0; k<a.size(); k++){
                if(result[i][j] == a[k] && out[k] == ""){
                    out[k] = name[i];
                    break;
                }
            }
        }
    }

    for(int k=0; k<a.size(); k++){
        cout << out[k];
    }


    return 0;
}
