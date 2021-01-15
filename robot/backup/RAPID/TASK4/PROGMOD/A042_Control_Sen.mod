MODULE A042_Control_Sen
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
    ! Date        :     2018.10.05
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
        ! Work process
        WHILE b_A042_Run=TRUE DO
            !
            ! Check and send data to client
            IF b_A042_Com{n_A042_R1_ChaNr}=TRUE THEN
                !
                ! For robot
                IF bm_A042_SenBufferRob{n_A042_R1_ChaNr,n_A042_ReadPtrSenBufRob{n_A042_R1_ChaNr}}.startbit=TRUE r_A042_PackSendDataToClient\Rob,n_A042_R1_ChaNr;
                !
                ! For master
                IF bm_A042_SenBufferMa{n_A042_R1_ChaNr,n_A042_ReadPtrSenBufMa{n_A042_R1_ChaNr}}.startbit=TRUE r_A042_PackSendDataToClient\Ma,n_A042_R1_ChaNr;
            ENDIF
            !
            ! Check and send data to client
            IF b_A042_Com{n_A042_R2_ChaNr}=TRUE THEN
                !
                ! For robot
                IF bm_A042_SenBufferRob{n_A042_R2_ChaNr,n_A042_ReadPtrSenBufRob{n_A042_R2_ChaNr}}.startbit=TRUE r_A042_PackSendDataToClient\Rob,n_A042_R2_ChaNr;
                !
                ! For master
                IF bm_A042_SenBufferMa{n_A042_R2_ChaNr,n_A042_ReadPtrSenBufMa{n_A042_R2_ChaNr}}.startbit=TRUE r_A042_PackSendDataToClient\Ma,n_A042_R2_ChaNr;
            ENDIF
            !
            ! Check and send data to client
            IF b_A042_Com{n_A042_R3_ChaNr}=TRUE THEN
                !
                ! For robot
                IF bm_A042_SenBufferRob{n_A042_R3_ChaNr,n_A042_ReadPtrSenBufRob{n_A042_R3_ChaNr}}.startbit=TRUE r_A042_PackSendDataToClient\Rob,n_A042_R3_ChaNr;
                !
                ! For master
                IF bm_A042_SenBufferMa{n_A042_R3_ChaNr,n_A042_ReadPtrSenBufMa{n_A042_R3_ChaNr}}.startbit=TRUE r_A042_PackSendDataToClient\Ma,n_A042_R3_ChaNr;
            ENDIF
            !
            ! Check and send data to client
            IF b_A042_Com{n_A042_R4_ChaNr}=TRUE THEN
                !
                ! For robot
                IF bm_A042_SenBufferRob{n_A042_R4_ChaNr,n_A042_ReadPtrSenBufRob{n_A042_R4_ChaNr}}.startbit=TRUE r_A042_PackSendDataToClient\Rob,n_A042_R4_ChaNr;
                !
                ! For master
                IF bm_A042_SenBufferMa{n_A042_R4_ChaNr,n_A042_ReadPtrSenBufMa{n_A042_R4_ChaNr}}.startbit=TRUE r_A042_PackSendDataToClient\Ma,n_A042_R4_ChaNr;
            ENDIF
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
    ! Date        :     2018.07.10
    !***************** ETH Zürich *******************
    !
    PROC r_A042_InitCell()
        !
        ! Task synchronisation 
        WaitSyncTask id_A042_InitSta,tl_A042_All;
        !
        ! Task synchronisation wait for master data 
        WaitSyncTask id_A042_InitMa,tl_A042_All;
        !
        ! Initialize variables
        r_A042_InitVar;
        !
        ! Initialize sockets
        IF b_A042_SocketActiv=TRUE r_A042_InitSockets;
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
        ! Set Task on
        b_A042_TaskSenderOn:=TRUE;
        !
        ! Reset and start timestamp
        ClkReset clk_A042_TimeStamp;
        ClkStart clk_A042_TimeStamp;
        !
        ! Reset Counters
        n_A042_WritePtrSenBufMa{n_A042_R1_ChaNr}:=0;
        n_A042_WritePtrSenBufMa{n_A042_R2_ChaNr}:=0;
        n_A042_WritePtrSenBufMa{n_A042_R3_ChaNr}:=0;
        n_A042_WritePtrSenBufMa{n_A042_R4_ChaNr}:=0;
        !
        n_A042_WritePtrSenBufRob{n_A042_R1_ChaNr}:=0;
        n_A042_WritePtrSenBufRob{n_A042_R2_ChaNr}:=0;
        n_A042_WritePtrSenBufRob{n_A042_R3_ChaNr}:=0;
        n_A042_WritePtrSenBufRob{n_A042_R4_ChaNr}:=0;
        !
        n_A042_ReadPtrSenBufMa{n_A042_R1_ChaNr}:=1;
        n_A042_ReadPtrSenBufMa{n_A042_R2_ChaNr}:=1;
        n_A042_ReadPtrSenBufMa{n_A042_R3_ChaNr}:=1;
        n_A042_ReadPtrSenBufMa{n_A042_R4_ChaNr}:=1;
        !
        n_A042_ReadPtrSenBufRob{n_A042_R1_ChaNr}:=1;
        n_A042_ReadPtrSenBufRob{n_A042_R2_ChaNr}:=1;
        n_A042_ReadPtrSenBufRob{n_A042_R3_ChaNr}:=1;
        n_A042_ReadPtrSenBufRob{n_A042_R4_ChaNr}:=1;
        !        
        n_A042_SenHeaderSqzNr{n_A042_R1_ChaNr}:=0;
        n_A042_SenHeaderSqzNr{n_A042_R2_ChaNr}:=0;
        n_A042_SenHeaderSqzNr{n_A042_R3_ChaNr}:=0;
        n_A042_SenHeaderSqzNr{n_A042_R4_ChaNr}:=0;
        !
        ! Clear Buffers
        FOR i FROM 1 TO DIM(bm_A042_SenBufferMa,2) DO
            !
            ! Overwrite with an empty message
            bm_A042_SenBufferMa{n_A042_R1_ChaNr,i}:=bmEmpty;
            bm_A042_SenBufferMa{n_A042_R2_ChaNr,i}:=bmEmpty;
            bm_A042_SenBufferMa{n_A042_R3_ChaNr,i}:=bmEmpty;
            bm_A042_SenBufferma{n_A042_R4_ChaNr,i}:=bmEmpty;
        ENDFOR
        !
        ! Clear Buffers
        FOR i FROM 1 TO DIM(bm_A042_SenBufferRob,2) DO
            !
            ! Overwrite with an empty message
            bm_A042_SenBufferRob{n_A042_R1_ChaNr,i}:=bmEmpty;
            bm_A042_SenBufferRob{n_A042_R2_ChaNr,i}:=bmEmpty;
            bm_A042_SenBufferRob{n_A042_R3_ChaNr,i}:=bmEmpty;
            bm_A042_SenBufferRob{n_A042_R4_ChaNr,i}:=bmEmpty;
        ENDFOR
        !
        ! Clear Buffers
        FOR i FROM 1 TO DIM(pro_A042_ActMsgSen,2) DO
            !
            ! Overwrite with an empty protocol
            pro_A042_ActMsgSen{1,i}:=proEmpty;
            pro_A042_ActMsgSen{1,i}:=proEmpty;
            pro_A042_ActMsgSen{1,i}:=proEmpty;
            pro_A042_ActMsgSen{1,i}:=proEmpty;
            !
            pro_A042_ActMsgSen{2,i}:=proEmpty;
            pro_A042_ActMsgSen{2,i}:=proEmpty;
            pro_A042_ActMsgSen{2,i}:=proEmpty;
            pro_A042_ActMsgSen{2,i}:=proEmpty;
        ENDFOR
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