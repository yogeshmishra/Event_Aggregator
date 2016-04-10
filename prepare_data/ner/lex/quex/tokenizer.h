struct tokenizer{
    quex_Token*  token_p;
    EasyLexer    qlex;
    char         buffer[1024];
};

typedef struct tokenizer Tokenizer;
Tokenizer* tokenizer_new(FILE *file_handler);
const char *next_token(Tokenizer *lexer);
void tokenizer_free(Tokenizer *lexer);
