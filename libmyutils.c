#include <stdio.h>

// 1. helloworld
int helloworld(void){
    printf("Hello World !\n");
    return 0;
}


// 2. pass two values
int sum(int a, int b){
    return a+b;
}


// 3. pass a pointer value
int pass_value_by_reference(int *value){
    int tmp = *value;
    *value = 321;
    printf("%d -> %d\n", tmp, *value);
    return 0;
}


// 4. pass a struct by value
typedef struct {
    int value;
    char str[100];
}pass_struct_by_value_t;

int pass_struct_by_value(pass_struct_by_value_t my_struct){
    printf("%d %s\n", my_struct.value, my_struct.str);
    return 0;
}


// 5. pass a pointer struct
typedef struct {
    int value;
    char str[100];
    int result;
}pass_struct_by_reference_t;

int pass_struct_by_reference(pass_struct_by_reference_t *my_struct_p){
    printf("%d %s\n", my_struct_p->value, my_struct_p->str);
    my_struct_p->result = 123;
    return 0;
}


// 6. pass a nested struct
typedef struct {
    char ip_address[64];
}ip_t;

typedef struct {
    char name[128];
    int ip_num;
    ip_t *ip;
}machine_t;

typedef struct {
    int machine_num;
    machine_t *machine;
}servers_t;

int show_servers(servers_t *servers){
    for(int i=0; i<servers->machine_num; i++){
        machine_t *machine = &servers->machine[i];
        for(int j=0; j<machine->ip_num; j++){
            printf("%s %s\n", machine->name, machine->ip[j].ip_address);
        }
    }
    return 0;
}


// 7. pass a function pointer
typedef void (*callback_func)(char *msg);
void callback_sample(callback_func callback){
    callback("Hello World !");
}