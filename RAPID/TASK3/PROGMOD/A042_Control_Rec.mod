MODULE A042_Control_Rec
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
        ! Wait until master has set taskliste all
        WaitTime n_A042_TimeTaskLiAll;
        !
        ! Task synchronisation 
        WaitSyncTask id_A042_MainSta,tl_A042_All;
        !
        ! Message for Operator
        TPWrite "A042 Main";
        !
        ! Initialize cell
        r_A042_InitCell;
        !
        ! Work process
        WHILE b_A042_Run=TRUE DO
            !
            ! Check and receive data from client 1
            IF b_A042_Com{n_A042_R1_ChaNr}=TRUE r_A042_CheckAndRecFrmClient n_A042_R1_ChaNr;
            !
            ! Check and receive data from client 2
            IF b_A042_Com{n_A042_R2_ChaNr}=TRUE r_A042_CheckAndRecFrmClient n_A042_R2_ChaNr;
            !
            ! Check and receive data from client 3
            IF b_A042_Com{n_A042_R3_ChaNr}=TRUE r_A042_CheckAndRecFrmClient n_A042_R3_ChaNr;
            !
            ! Check and receive data from client 4
            IF b_A042_Com{n_A042_R4_ChaNr}=TRUE r_A042_CheckAndRecFrmClient n_A042_R4_ChaNr;
            !
            ! Check cycle time stop watch activ 
            IF b_A042_EvLogMsgInUntilMsgOutTime=TRUE THEN
                !
                ! Measure cycle time
                IF b_A042_FeedbackOut=TRUE THEN
                    !
                    ! Reset variable
                    b_A042_FeedbackOut:=FALSE;
                    !
                    ! Stop read message input to feedback done watch
                    ClkStop clk_A042_MsgInUntilMsgOut;
                    !
                    ! Log current read and unpack time in RobotStudio output
                    r_A042_EvLogMsg st_A042_EvLogMsgHeader,"Msg in until Msg out time : "+NumToStr(ClkRead(clk_A042_MsgInUntilMsgOut\HighRes),3);
                ENDIF
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
        ! Initalize protocol log
        !* r_A042_LogProtInit;
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
        b_A042_TaskReceiverOn:=TRUE;
        !
        ! Reset buffer full bits master
        b_A042_BufFullMa{n_A042_R1_ChaNr}:=FALSE;
        b_A042_BufFullMa{n_A042_R2_ChaNr}:=FALSE;
        b_A042_BufFullMa{n_A042_R3_ChaNr}:=FALSE;
        b_A042_BufFullMa{n_A042_R4_ChaNr}:=FALSE;
        !
        ! Reset buffer full bits robot
        b_A042_BufFullRob{n_A042_R1_ChaNr}:=FALSE;
        b_A042_BufFullRob{n_A042_R2_ChaNr}:=FALSE;
        b_A042_BufFullRob{n_A042_R3_ChaNr}:=FALSE;
        b_A042_BufFullRob{n_A042_R4_ChaNr}:=FALSE;
        !
        ! Set first cycle bools 
        b_A042_FirstProtocolAfterPPMain:=TRUE;
        !
        ! Temp to measure cycle time
        b_A042_FeedbackOut:=FALSE;


        !
        ! Reset Counters master
        n_A042_WritePtrBufMa{n_A042_R1_ChaNr}:=0;
        n_A042_WritePtrBufMa{n_A042_R2_ChaNr}:=0;
        n_A042_WritePtrBufMa{n_A042_R3_ChaNr}:=0;
        n_A042_WritePtrBufMa{n_A042_R4_ChaNr}:=0;
        !
        ! Reset Counters robot 
        n_A042_WritePtrBufRob{n_A042_R1_ChaNr}:=0;
        n_A042_WritePtrBufRob{n_A042_R2_ChaNr}:=0;
        n_A042_WritePtrBufRob{n_A042_R3_ChaNr}:=0;
        n_A042_WritePtrBufRob{n_A042_R4_ChaNr}:=0;
        !
        ! Clear Buffer master
        FOR i FROM 1 TO DIM(bm_A042_RecBufferMa,2) DO
            !
            ! Overwrite with an empty message
            bm_A042_RecBufferMa{n_A042_R1_ChaNr,i}:=bmEmpty;
            bm_A042_RecBufferMa{n_A042_R2_ChaNr,i}:=bmEmpty;
            bm_A042_RecBufferMa{n_A042_R3_ChaNr,i}:=bmEmpty;
            bm_A042_RecBufferMa{n_A042_R4_ChaNr,i}:=bmEmpty;
            !
        ENDFOR
        !
        ! Clear Buffer robots
        FOR i FROM 1 TO DIM(bm_A042_RecBufferRob,2) DO
            !
            ! Overwrite with an empty message
            bm_A042_RecBufferRob{n_A042_R1_ChaNr,i}:=bmEmpty;
            bm_A042_RecBufferRob{n_A042_R2_ChaNr,i}:=bmEmpty;
            bm_A042_RecBufferRob{n_A042_R3_ChaNr,i}:=bmEmpty;
            bm_A042_RecBufferRob{n_A042_R4_ChaNr,i}:=bmEmpty;
            !
        ENDFOR
        !
        ! Reset expected Sequince ID
        n_A042_SIDExpected{n_A042_R1_ChaNr}:=0;
        n_A042_SIDExpected{n_A042_R2_ChaNr}:=0;
        n_A042_SIDExpected{n_A042_R3_ChaNr}:=0;
        n_A042_SIDExpected{n_A042_R4_ChaNr}:=0;
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