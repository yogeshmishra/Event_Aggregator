#include <stdio.h>    
#include "EasyLexer.h"
#include "tokenizer.h"

#ifndef     ENCODING_NAME
#    define ENCODING_NAME (0x0)
#endif

const size_t BufferSize = 1024;


Tokenizer* tokenizer_init_file(FILE *file_handler){
    Tokenizer * lexer;
    lexer = (Tokenizer *) malloc(sizeof(Tokenizer));
    lexer->token_p = 0x0;
    QUEX_NAME(construct_FILE)(&lexer->qlex, file_handler, ENCODING_NAME, false);
    return lexer;
}

Tokenizer* tokenizer_init_string(QUEX_TYPE_CHARACTER* str){
    Tokenizer * lexer;
    char* qlex_buffer = 0x0;

    lexer = (Tokenizer *) malloc(sizeof(Tokenizer));
    lexer->token_p = 0x0;
    QUEX_TYPE_CHARACTER* start = str+sizeof(QUEX_TYPE_CHARACTER);
    size_t chars_num = strlen(str);
    size_t bufsize = sizeof(str);
    QUEX_NAME(construct_memory)(&lexer->qlex, str, bufsize,
                                bufsize, ENCODING_NAME, false);
/*    QUEX_NAME(construct_memory)(&lexer->qlex, 0x0, 0, 0X0, ENCODING_NAME, false);*/
    /*QUEX_NAME(construct_memory)(&lexer->qlex, str, memory_size, str+memory_size,
                                ENCODING_NAME, false);*/
    QUEX_NAME(buffer_fill_region_prepare)(&lexer->qlex);
/*    qlex_buffer      = (char*)QUEX_NAME(buffer_fill_region_begin)(&lexer->qlex);
    size_t qlex_buffer_size = QUEX_NAME(buffer_fill_region_size(&lexer->qlex));
    memcpy(qlex_buffer, str, qlex_buffer_size);*/
    QUEX_NAME(buffer_fill_region_finish)(&lexer->qlex, chars_num);
    return lexer;
}

const char* next_token(Tokenizer *lexer){
    QUEX_NAME(receive)(&lexer->qlex, &lexer->token_p);
    return QUEX_NAME_TOKEN(pretty_char_text)(lexer->token_p, lexer->buffer, BufferSize);
}

void tokenizer_free(Tokenizer *lexer){
    QUEX_NAME(destruct)(&lexer->qlex);
}

QUEX_TYPE_CHARACTER* read_file(FILE *fh){
  unsigned long lSize;
  QUEX_TYPE_CHARACTER* buffer;
  size_t result;
  
  if (fh==NULL) {fputs ("File error",stderr); exit (1);}

  /* obtain file size: */
  fseek(fh , 0 , SEEK_END);
  lSize = ftell(fh);
  rewind(fh);

  /* allocate memory to contain the whole file:*/
  buffer = (QUEX_TYPE_CHARACTER*) malloc (sizeof(QUEX_TYPE_CHARACTER)*(lSize));
  QUEX_TYPE_CHARACTER* buffer_start = sizeof(QUEX_TYPE_CHARACTER)+buffer;
  if (buffer == NULL) {fputs ("Memory error",stderr); exit (2);}

  /* copy the file into the buffer:*/
  result = fread (buffer_start, 1, lSize, fh);
  if (result != lSize) {fputs ("Reading error",stderr); exit (3);}
  return buffer;
}

int main(int argc, char** argv) 
{        
    FILE *fh = fdopen(0, "r");
    Tokenizer * lexer = tokenizer_init_file(fh);
/*    QUEX_TYPE_CHARACTER* string = read_file(fh);*/
/*    printf("%s", string+sizeof(QUEX_TYPE_CHARACTER));*/
/*    Tokenizer * lexer = tokenizer_init_string(string);*/
    do{
        printf("%s ", next_token(lexer)); 
    } while( lexer->token_p->_id != QUEX_TKN_TERMINATION );
    tokenizer_free(lexer);
    /* free(string);*/
    return 0;
}
