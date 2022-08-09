#include <iostream>
using namespace std;

class Chess{
    private:
    string chess_board[8][8] = {
        {"wr1", "wh1", "wb1", "wk", "wq", "wb2", "wh2", "wr2"},
        {"wp1", "wp2", "wp3", "wp4", "wp5", "wp6", "wp7", "wp8"},
        {"", "", "", "", "", "", "", ""},
        {"", "", "", "", "", "", "", ""},
        {"", "", "", "", "", "", "", ""},
        {"", "", "", "", "", "", "", ""},
        {"bp1", "bp2", "bp3", "bp4", "bp5", "bp6", "bp7", "bp8"},
        {"br1", "bh1", "bb1", "bk", "bq", "bb2", "bh2", "br2"},
    };
    
    public:
    void display_board(){
        for(int i = 0; i < 8; i++){
            for(int j = 0; j < 8; j++){
                cout << chess_board[i][j] << " ";
            }
            cout << endl;
        }
    }
};

int main()
{
    Chess c;
    c.display_board();

    return 0;
}
