      INTEGER FUNCTION test()
        IMPLICIT NONE
        INCLUDE "acc_testsuite.f90"
        TYPE multi_item
          REAL(8) :: a
          REAL(8) :: b
          REAL(8) :: c
        END TYPE multi_item
        INTEGER :: x !Iterators
        TYPE (multi_item),DIMENSION(LOOPCOUNT):: a !Data
        INTEGER :: errors = 0

        !Initilization
        CALL RANDOM_SEED()
        DO x = 1, LOOPCOUNT
          CALL RANDOM_NUMBER(a(x)%a)
          CALL RANDOM_NUMBER(a(x)%b)
          a(x)%c = 0.0
        END DO

        !$acc data copy(a(1:LOOPCOUNT))
          !$acc parallel
            !$acc loop
            DO x = 1, LOOPCOUNT
              a(x)%c = a(x)%a + a(x)%b
            END DO
          !$acc end parallel
        !$acc end data
        DO x = 1, LOOPCOUNT
          IF (abs(a(x)%c - (a(x)%a + a(x)%b)) .gt. PRECISION) THEN
            errors = errors + 1
          END IF
        END DO
        test = errors
      END


      PROGRAM test_kernels_async_main
      IMPLICIT NONE
      INTEGER :: failed, success !Number of failed/succeeded tests
      INTEGER :: num_tests,crosschecked, crossfailed, j
      INTEGER :: temp,temp1
      INCLUDE "acc_testsuite.f90"
      INTEGER test


      CHARACTER*50:: logfilename !Pointer to logfile
      INTEGER :: result

      num_tests = 0
      crosschecked = 0
      crossfailed = 0
      result = 1
      failed = 0

      !Open a new logfile or overwrite the existing one.
      logfilename = "test.log"
!      WRITE (*,*) "Enter logFilename:"
!      READ  (*,*) logfilename

      OPEN (1, FILE = logfilename)

      WRITE (*,*) "######## OpenACC Validation Suite V 2.5 ######"
      WRITE (*,*) "## Repetitions:", N
      WRITE (*,*) "## Loop Count :", LOOPCOUNT
      WRITE (*,*) "##############################################"
      WRITE (*,*)

      WRITE (*,*) "--------------------------------------------------"
      WRITE (*,*) "Test of data_with_derived_type"
      WRITE (*,*) "--------------------------------------------------"

      crossfailed=0
      result=1
      WRITE (1,*) "--------------------------------------------------"
      WRITE (1,*) "Test of data_with_derived_type"
      WRITE (1,*) "--------------------------------------------------"
      WRITE (1,*)
      WRITE (1,*) "(Crosstests should fail)"
      WRITE (1,*)

      DO j = 1, N
        temp =  test()
        IF (temp .EQ. 0) THEN
          WRITE (1,*)  j, ". test successfull."
          success = success + 1
        ELSE
          WRITE (1,*) "Error: ",j, ". test failed."
          failed = failed + 1
        ENDIF
      END DO


      IF (failed .EQ. 0) THEN
        WRITE (1,*) "Directive worked without errors."
        WRITE (*,*) "Directive worked without errors."
        result = 0
        WRITE (*,*) "Result:",result
      ELSE
        WRITE (1,*) "Directive failed the test ", failed, " times."
        WRITE (*,*) "Directive failed the test ", failed, " times."
        result = failed * 100 / N
        WRITE (*,*) "Result:",result
      ENDIF
      CALL EXIT (result)
      END PROGRAM
                                             

