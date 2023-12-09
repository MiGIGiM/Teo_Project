int func1(int a, int b){
    return (a + b);
}

char func2(char a, char b) {
    return (a + b);
}

int main() {
    int a, b = 2 , c ;
    char c1 = 'a', c2;
    func2(c1, 'D');
    string str = 'hola' + 'c';
    float d;
    d = 2.2;
    a = b / 3;
    c = 5 * b;

    if(a != b){
        a = b;
    }
    else if( c1 > 0 && c > b){
        c2 = 'b';
    }
    else{
        c = c + 1 ;
    }

    while( c > b || c > a){
        c = c - 2;
        if( c < 0 &&  c != (2 * b) / 5 ){
            return c;
        }
        else{
            return func1(a,c);
        }
    }
}
