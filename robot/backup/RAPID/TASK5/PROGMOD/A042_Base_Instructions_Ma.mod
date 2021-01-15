MODULE A042_Base_Instructions_Ma
    !***********************************************************************************
    !
    ! ETH Zürich / Robotic Fabrication Lab
    ! HIB C 13 / Stefano-Franscini-Platz 1
    ! CH-8093 Zürich
    !
    !***********************************************************************************
    !
    ! PROJECT     :  A042 Driver
    !
    ! FUNCTION    :  Base Instracion Library for master  
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2020.02.21 Draft
    !
    ! Copyright   :  ETH Zürich (CH) 2018
    !                - Philippe Fleischmann
    !                - Michael Lyrenmann
    !                - Gonzalo Casas
    !
    ! License     :  You agree that the software source code and documentation
    !                provided by the copyright holder is confidential, 
    !                and you shall take all reasonable precautions to protect
    !                the source code and documentation, and preserve its confidential,
    !                proprietary and trade secret status in perpetuity. 
    ! 
    !                This license is strictly limited to INTERNAL use within one site.
    !
    !***********************************************************************************

    !************************************************
    ! Function    :     Dummy
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2020.02.21
    !***************** ETH Zürich *******************
    !
    PROC r_A042_Dummy()
        !
        ! Just a dummy procedure for communication tests
        !
        ! Read the current Sequnce ID
        n_A042_Act_S_ID:=bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.S_ID;
        !
        ! Feedback
        IF bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.F_Lev>0 THEN
            !
            ! Cenerate feedback
            TEST bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.F_Lev
            CASE 1:
                !nChaNr
                ! Instruction done 
                r_A042_FDone;
            DEFAULT:
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufMa n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Read actual jointtarget
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Zürich *******************
    !
    PROC r_A042_GetJointT()
        !
        ! Read current joint position
        jp_A042_Act:=CJointT(\TaskName:=st_A042_ChaTask);
        !
        ! Add robot axis values to feedback
        r_A042_FAddValue jp_A042_Act.robax.rax_1;
        r_A042_FAddValue jp_A042_Act.robax.rax_2;
        r_A042_FAddValue jp_A042_Act.robax.rax_3;
        r_A042_FAddValue jp_A042_Act.robax.rax_4;
        r_A042_FAddValue jp_A042_Act.robax.rax_5;
        r_A042_FAddValue jp_A042_Act.robax.rax_6;
        !
        ! Add external axis values to feedback
        r_A042_FAddValue jp_A042_Act.extax.eax_a;
        r_A042_FAddValue jp_A042_Act.extax.eax_b;
        r_A042_FAddValue jp_A042_Act.extax.eax_c;
        r_A042_FAddValue jp_A042_Act.extax.eax_d;
        r_A042_FAddValue jp_A042_Act.extax.eax_e;
        r_A042_FAddValue jp_A042_Act.extax.eax_f;
        !
        ! Add cyclic feedback instruction done
        r_A042_CyFDone;
        !
        ! Feedback
        IF bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.F_Lev>1 THEN
            !
            ! Check additional feedback
            TEST bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.F_Lev
            CASE 10001:
                !
                ! add robot position  
                !* r_A042_FPos bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev;
            DEFAULT:
                !
                ! Not defined 
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
        ENDIF
        !
        ! Move message in send buffer
        r_A042_MovMsgToSenBufMa n_A042_ChaNr;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Get robtarget  
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.20
    !***************** ETH Zï¿½rich *******************
    !
    PROC r_A042_GetRobT()
        !
        ! Read current joint position
        p_A042_Act:=CRobT(\TaskName:=st_A042_ChaTask);
        !
        ! Add translastion values to feedback
        r_A042_FAddValue p_A042_Act.trans.x;
        r_A042_FAddValue p_A042_Act.trans.y;
        r_A042_FAddValue p_A042_Act.trans.z;
        !
        ! Add rotation values to feedback
        r_A042_FAddValue p_A042_Act.rot.q1;
        r_A042_FAddValue p_A042_Act.rot.q2;
        r_A042_FAddValue p_A042_Act.rot.q3;
        r_A042_FAddValue p_A042_Act.rot.q4;
        !
        ! Add external axis values to feedback
        r_A042_FAddValue p_A042_Act.extax.eax_a;
        r_A042_FAddValue p_A042_Act.extax.eax_b;
        r_A042_FAddValue p_A042_Act.extax.eax_c;
        r_A042_FAddValue p_A042_Act.extax.eax_d;
        r_A042_FAddValue p_A042_Act.extax.eax_e;
        r_A042_FAddValue p_A042_Act.extax.eax_f;
        !
        ! Add standard feedback instruction done
        r_A042_FDone;
        !
        ! Feedback
        IF bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.F_Lev>1 THEN
            !
            ! Check additional feedback
            TEST bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.F_Lev
            CASE 10001:
                !
                ! add robot position  
                !* r_A042_FPos bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev;
            DEFAULT:
                !
                ! Not defined 
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
        ENDIF
        !
        ! Move message in send buffer
        r_A042_MovMsgToSenBufMa n_A042_ChaNr;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Stop
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.08.27
    !***************** ETH Zürich *******************
    !
    PROC r_A042_Stop()
        !
        ! Stop task
        Stop;
        !
        ! Feedback
        IF bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.F_Lev>0 THEN
            !
            ! Cenerate feedback
            TEST bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.F_Lev
            CASE 1:
                !
                ! Instruction done 
                r_A042_FDone;
            DEFAULT:
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufMa n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Teachpendant Write
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.10.14
    !***************** ETH Zürich *******************
    !
    PROC r_A042_TPWrite()
        !
        ! Read acceleration
        st_A042_TPWrite{n_A042_ChaNr}:=bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.St1;
        !
        ! Clear panel 
        TPErase;
        !
        ! Show message to user 
        TPWrite st_A042_TPWrite{n_A042_ChaNr};
        !
        ! Feedback
        IF bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.F_Lev>0 THEN
            !
            ! Cenerate feedback
            TEST bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.F_Lev
            CASE 1:
                !
                ! Instruction done 
                r_A042_FDone;
            DEFAULT:
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufMa n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Cyclic job start
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2020.02.27
    !***************** ETH Zürich *******************
    !
    PROC r_A042_CyJobStart()
        !
        ! Read cyclic jop Sqz_ID
        n_A042_CyJobStart_S_ID{n_A042_ChaNr}:=bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.S_ID;
        !
        ! Read cyclic job
        st_A042_CyclicJob{n_A042_ChaNr}:=bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.St1;
        !
        ! Read cycle minimal time
        n_A042_MinCycleTime{n_A042_ChaNr}:=bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.V1;
        !
        ! Activate cyclic job
        b_A042_CyclicJob{n_A042_ChaNr}:=TRUE;
        !
        ! Start cycle clock 
        ClkStart ck_A042_CycleJob{n_A042_ChaNr};
        !
        ! Feedback
        IF bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.F_Lev>0 THEN
            !
            ! Cenerate feedback
            TEST bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.F_Lev
            CASE 1:
                !nChaNr
                ! Instruction done 
                r_A042_FDone;
            DEFAULT:
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufMa n_A042_ChaNr;
        ENDIF
        !
        ! Event log message  
        r_A042_EvLogMsg st_A042_EvLogMsgHeader,"Cyclic job channel "+NumToStr(n_A042_ChaNr,0)+" started with job: "+st_A042_CyclicJob{n_A042_ChaNr};
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Cyclic job end
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2020.02.27
    !***************** ETH Zürich *******************
    !
    PROC r_A042_CyJobEnd()
        !
        ! Stop and reset cycle clock 
        ClkStop ck_A042_CycleJob{n_A042_ChaNr};
        ClkReset ck_A042_CycleJob{n_A042_ChaNr};
        !
        ! Deactivate cyclic job
        b_A042_CyclicJob{n_A042_ChaNr}:=FALSE;
        !
        ! Feedback
        IF bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.F_Lev>0 THEN
            !
            ! Cenerate feedback
            TEST bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.F_Lev
            CASE 1:
                !nChaNr
                ! Instruction done 
                r_A042_FDone;
            DEFAULT:
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufMa n_A042_ChaNr;
        ENDIF
        !
        ! Event log message  
        r_A042_EvLogMsg st_A042_EvLogMsgHeader,"Cyclic job channel "+NumToStr(n_A042_ChaNr,0)+" ended with job: "+st_A042_CyclicJob{n_A042_ChaNr};
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Cyclic job test
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2020.02.27
    !***************** ETH Zürich *******************
    !
    PROC r_A042_CyJobTest()
        !
        ! Increase cycle time
        Incr n_A042_ActCycle{n_A042_ChaNr};
        !
        ! Write cycle number and ccurrent cycle time
        TPWrite "Cycle Nr: "+NumToStr(n_A042_ActCycle{n_A042_ChaNr},0)+" Cycle Time: "+NumToStr(n_A042_LastCycleTime{n_A042_ChaNr},3);
        !
        ! Feedback
        IF bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.F_Lev>0 THEN
            !
            ! Cenerate feedback
            TEST bm_A042_RecBufferMa{n_A042_ChaNr,n_A042_ReadPtrRecBuf{n_A042_ChaNr}}.Data.F_Lev
            CASE 1:
                !nChaNr
                ! Instruction done 
                r_A042_FDone;
            DEFAULT:
                !
                ! Feedback not supported  
                r_A042_FError;
            ENDTEST
            !
            ! Move message in send buffer
            r_A042_MovMsgToSenBufMa n_A042_ChaNr;
        ENDIF
        !
        ! Event log message  
        r_A042_EvLogMsg st_A042_EvLogMsgHeader,"Cyclic job channel "+NumToStr(n_A042_ChaNr,0)+" running with job: "+st_A042_CyclicJob{n_A042_ChaNr};
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC
ENDMODULE