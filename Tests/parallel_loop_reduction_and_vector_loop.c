#include "acc_testsuite.h"

int test(){
    int err = 0;
    srand(time(NULL));
    char * a = (char *)malloc(10 * n * sizeof(char));
    char * b = (char *)malloc(10 * sizeof(char));
    char * has_false = (char *)malloc(10 * sizeof(char));
    for (int x = 0; x < 10; ++x){
        has_false[x] = 0;
    }
    real_t false_margin = pow(exp(1), log(.5)/n);
    for (int x = 0; x < 10 * n; ++x){
        if(rand() / (real_t)(RAND_MAX) < false_margin){
            a[x] = 1;
        }
        else{
            a[x] = 0;
            has_false[x/n] = 1;
        }
    }
    char temp = 1;
    #pragma acc data copyin(a[0:10*n]) copy(b[0:10])
    {
        #pragma acc parallel loop private(temp)
        for (int x = 0; x < 10; ++x){
            temp = 1;
            #pragma acc loop vector reduction(&&:temp)
            for (int y = 0; y < n; ++y){
                temp = temp && a[x * n + y];
            }
            b[x] = temp;
        }
    }
    for (int x = 0; x < 10; ++x){
        if (has_false[x] == b[x]){
            err = 1;
        }
    }

    free(a);
    free(b);
    free(has_false);
    return err;
}


int main()
{
  int i;                        /* Loop index */
  int result;           /* return value of the program */
  int failed=0;                 /* Number of failed tests */
  int success=0;                /* number of succeeded tests */
  static FILE * logFile;        /* pointer onto the logfile */
  static const char * logFileName = "test_acc_lib_acc_wait.log";        /* name of the logfile */


  /* Open a new Logfile or overwrite the existing one. */
  logFile = fopen(logFileName,"w+");

  printf("######## OpenACC Validation Suite V %s #####\n", ACCTS_VERSION );
  printf("## Repetitions: %3d                       ####\n",REPETITIONS);
  printf("## Array Size : %.2f MB                 ####\n",ARRAYSIZE * ARRAYSIZE/1e6);
  printf("##############################################\n");
  printf("Testing parallel_loop_reduction_and_vector_loop\n\n");

  fprintf(logFile,"######## OpenACC Validation Suite V %s #####\n", ACCTS_VERSION );
  fprintf(logFile,"## Repetitions: %3d                       ####\n",REPETITIONS);
  fprintf(logFile,"## Array Size : %.2f MB                 ####\n",ARRAYSIZE * ARRAYSIZE/1e6);
  fprintf(logFile,"##############################################\n");
  fprintf(logFile,"Testing parallel_loop_reduction_and_vector_loop\n\n");

  for ( i = 0; i < REPETITIONS; i++ ) {
    fprintf (logFile, "\n\n%d. run of parallel_loop_reduction_and_vector_loop out of %d\n\n",i+1,REPETITIONS);
    if (test() == 0) {
      fprintf(logFile,"Test successful.\n");
      success++;
    } else {
      fprintf(logFile,"Error: Test failed.\n");
      printf("Error: Test failed.\n");
      failed++;
    }
  }

  if(failed==0) {
    fprintf(logFile,"\nDirective worked without errors.\n");
    printf("Directive worked without errors.\n");
    result=0;
  } else {
    fprintf(logFile,"\nDirective failed the test %i times out of %i. %i were successful\n",failed,REPETITIONS,success);
    printf("Directive failed the test %i times out of %i.\n%i test(s) were successful\n",failed,REPETITIONS,success);
    result = (int) (((double) failed / (double) REPETITIONS ) * 100 );
  }
  printf ("Result: %i\n", result);
  return result;
}

