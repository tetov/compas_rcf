MODULE A042_Control_Rob
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
    ! FUNCTION    :  Control modul for the project 
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2018.06.17 Draft
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
    ! Function    :     Main for Project A042
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2018.06.28
    ! **************** ETH Zürich *******************
    !
    PROC r_A042_Main()
        !
        ! wait until master has set taskliste all
        WaitTime n_A042_TimeTaskLiAll;
        !
        ! Task synchronisation 
        WaitSyncTask id_A042_MainSta,tl_A042_All;
        !
        ! Message for Operator
        TPWrite "A042 Main";
        !
        ! Inititalize cell 
        r_A042_InitCell;
        !
        ! Production loop
        WHILE b_A042_Run=TRUE DO
            !
            ! Wait for job in receiver buffer
            WaitUntil bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.startbit=TRUE\PollRate:=n_A042_PulRatWaiJobRec;
            !
            ! Execute job from receiver buffer
            r_A042_ExeJobFrmRecBuf;
        ENDWHILE
        !
        ! Message for Operator
        TPWrite "A042 End";
        !
        ! Task synchronisation 
        WaitSyncTask id_A042_MainEnd,tl_A042_All;
        !
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Initialize Cell
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2018.06.28
    ! **************** ETH Zürich *******************
    !
    PROC r_A042_InitCell()
        !
        ! Task synchronisation 
        WaitSyncTask id_A042_InitSta,tl_A042_All;
        !
        ! Task synchronisation wait for master data 
        WaitSyncTask id_A042_InitMa,tl_A042_All;
        !
        ! Initialize Variables
        r_A042_InitVar;
        !
        ! Connect Alias Signals from Tool
        !
        ! Task synchronisation 
        WaitSyncTask id_A042_InitEnd,tl_A042_All;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Initialize Variables
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2018.07.10
    !***************** ETH Zürich *******************
    !
    PROC r_A042_InitVar()
        !
        ! Reset Read pointer 
        n_A042_ReadPtrRecBuf:=1;
        !
        ! Reset Counter Feedback Value
        n_A042_CounterFStr:=0;
        !
        ! Reset Counter Feedback Value
        n_A042_CounterFVal:=0;
        !
        ! Clear actual sending message
        bm_A042_ActSenMsgRob:=bm_A042_Empty;
        !
        ! Read Taskname 
        st_A042_Taskname:=GetTaskName();
        !
        ! Set channel number
        TEST st_A042_Taskname
        CASE ch_A042_Channels.Ch_1.T_Name:
            !
            ! Set channel nuber to task
            n_A042_ChaNr:=ch_A042_Channels.Ch_1.Ch_Nr;
            !
        CASE ch_A042_Channels.Ch_2.T_Name:
            !
            ! Set channel nuber to task
            n_A042_ChaNr:=ch_A042_Channels.Ch_2.Ch_Nr;
            !
        CASE ch_A042_Channels.Ch_3.T_Name:
            !
            ! Set channel nuber to task
            n_A042_ChaNr:=ch_A042_Channels.Ch_3.Ch_Nr;
            !
        CASE ch_A042_Channels.Ch_4.T_Name:
            !
            ! Set channel nuber to task
            n_A042_ChaNr:=ch_A042_Channels.Ch_4.Ch_Nr;
            !
        DEFAULT:
            !
            ! Programm error
            r_A042_ProgError;
        ENDTEST
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Activate a job for the master 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2018.06.28
    !***************** ETH Zürich *******************
    !
    PROC r_A042_JobForMaster(string stJob)
        !
        ! Reserve master
        WaitTestAndSet b_A042_MaInUse;
        !
        ! Send job to master
        st_A042_JobForMa:=stJob;
        !
        ! Start jop for master
        b_A042_MaWaitForJob:=FALSE;
        !
        ! Wait until master is finish with job
        WaitUntil b_A042_MaWaitForJob=TRUE;
        !
        ! Release master
        b_A042_MaInUse:=FALSE;
        !
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Execute job from reveicer buffer
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2018.07.11
    !***************** ETH Zürich *******************
    !
    PROC r_A042_ExeJobFrmRecBuf()
        !
        ! Call instruction 
        %bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.Data.Instr %;
        !
        ! Set job done
        bm_A042_RecBufferRob{n_A042_ChaNr,n_A042_ReadPtrRecBuf}.startbit:=FALSE;
        !
        ! Count read pointer
        IF n_A042_ReadPtrRecBuf<DIM(bm_A042_RecBufferRob,2) THEN
            !
            ! Increas write pointer form buffer
            Incr n_A042_ReadPtrRecBuf;
        ELSE
            !
            ! Restart with one
            n_A042_ReadPtrRecBuf:=1;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !    !************************************************
    !    ! Function    :     Move message to send buffer roboter 1
    !    ! Programmer  :     Philippe Fleischmann
    !    ! Date        :     2018.07.09
    !    !***************** ETH Zürich *******************
    !    !
    !    PROC r_A042_MovMsgToSenBufRob1()
    !        !
    !        ! Count buffer pointer
    !        IF n_A042_WritePtrSenBufRob1<DIM(bm_A042_SenBufferRob1,1) THEN
    !            !
    !            ! Increas write pointer form buffer
    !            Incr n_A042_WritePtrSenBufRob1;
    !        ELSE
    !            !
    !            ! Restart with one
    !            n_A042_WritePtrSenBufRob1:=1;
    !        ENDIF
    !        !
    !        ! Check for bufferline free to write 
    !        IF NOT bm_A042_SenBufferRob1{n_A042_WritePtrSenBufRob1}.startbit=FALSE THEN
    !            !
    !            ! Wait for bufferline free to write 
    !            WaitUntil bm_A042_SenBufferRob1{n_A042_WritePtrSenBufRob1}.startbit=FALSE\PollRate:=0.004\Visualize\Header:="A042 MovMsgToSenBufRob1"\Message:="Buffer full"\Icon:=iconInfo;
    !        ENDIF
    !        !
    !        ! Write data in buffer
    !       bm_A042_SenBufferRob1{n_A042_WritePtrSenBufRob1}.Data:=bm_A042_ActSenMsgRob.Data;
    !        !
    !        ! Set Startbit
    !        bm_A042_SenBufferRob1{n_A042_WritePtrSenBufRob1}.startbit:=TRUE;
    !        !
    !        ! Clear actual sending message
    !        bm_A042_ActSenMsgRob:=bm_A042_Empty;
    !        RETURN ;
    !    ERROR
    !        ! Placeholder for Error Code...
    !    ENDPROC

    !************************************************
    ! Function    :     Move message to send buffer roboter 1
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2018.07.09
    !***************** ETH Zürich *******************
    !
    PROC r_A042_MovMsgToSenBufRob(num nChaNr)
        !
        ! Count buffer pointer
        IF n_A042_WritePtrSenBufRob{nChaNr}<DIM(bm_A042_SenBufferRob,2) THEN
            !
            ! Increas write pointer form buffer
            Incr n_A042_WritePtrSenBufRob{nChaNr};
        ELSE
            !
            ! Restart with one
            n_A042_WritePtrSenBufRob{nChaNr}:=1;
        ENDIF
        !
        ! Check for bufferline free to write 
        IF NOT bm_A042_SenBufferRob{nChaNr,n_A042_WritePtrSenBufRob{nChaNr}}.startbit=FALSE THEN
            !
            ! Wait for bufferline free to write 
            WaitUntil bm_A042_SenBufferRob{nChaNr,n_A042_WritePtrSenBufRob{nChaNr}}.startbit=FALSE\PollRate:=0.004;
        ENDIF
        !
        ! Write data in buffer
        bm_A042_SenBufferRob{nChaNr,n_A042_WritePtrSenBufRob{nChaNr}}.Data:=bm_A042_ActSenMsgRob.Data;
        !
        ! Set Startbit
        bm_A042_SenBufferRob{nChaNr,n_A042_WritePtrSenBufRob{nChaNr}}.startbit:=TRUE;
        !
        ! Clear actual sending message
        bm_A042_ActSenMsgRob:=bm_A042_Empty;
        !
        ! Reset Counter Feedback String and Value
        n_A042_CounterFStr:=0;
        n_A042_CounterFVal:=0;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     ProgError
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.11
    ! **************** ETH Zürich *******************
    !
    PROC r_A042_ProgError()
        ! 
        ! User Info
        TPWrite "Program Error";
        !
        ! Stop Program
        Stop;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

ENDMODULE