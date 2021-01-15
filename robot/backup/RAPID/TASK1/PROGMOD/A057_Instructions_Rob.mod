MODULE A057_Instructions_Rob
    !***********************************************************************************
    !
    ! ETH Zurich / NCCR Digital Fabrication
    ! HIB C51 / Stefano-Franscini-Platz 1
    ! CH-8093 Zürich
    !
    !***********************************************************************************
    !
    ! PROJECT     :  A057 MAS Rio
    !
    ! FUNCTION    :  Project specific procedures.
    !
    ! AUTHOR      :  Anton T Johansson
    !
    ! EMAIL       :  johansson@arch.ethz.ch
    !
    ! HISTORY     :  2020.11.06
    !
    ! Copyright   :  ETH Zürich (CH) 2020
    !
    !***********************************************************************************
    PROC r_A057_StopAll()
        !
        ! Stop task
        Stop \AllMoveTasks;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Cenerate feedback
            TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
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
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    PROC r_A057_TPWriteNoErase()
        !
        ! Read Text 
        st_A042_TPWrite:=bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.St1;
        !
        ! Clear panel 
        !TPErase;
        !
        ! Show message to user 
        TPWrite st_A042_TPWrite;
        !
        ! Feedback
        IF bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Cenerate feedback
            TEST bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.F_Lev
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
            r_A042_MovMsgToSenBufRob n_A042_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

ENDMODULE