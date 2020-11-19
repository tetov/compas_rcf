MODULE A052_Control
    !***********************************************************************************
    !
    ! ETH Zürich / Robotic Fabrication Lab
    ! HIB C 13 / Stefano-Franscini-Platz 1
    ! CH-8093 Zürich
    !
    !***********************************************************************************
    !
    ! PROJECT     :  A052 Robot Beefer
    !
    ! FUNCTION    :  Control of grill time   
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2019.03.28 Draft
    !
    ! Copyright   :  ETH Zürich (CH) 2018
    !                - Philippe Fleischmann
    !                - Michael Lyrenmann
    !                - Matthias Kohler 
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
    ! Function    :     Main for Project A052
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.07.29
    ! **************** ETH Zürich *******************
    !
    PROC main()
        !
        ! Initialize cell
        r_A052_InitCell;
        !
        ! Production loop
        WHILE b_A052_Run=TRUE DO
            !
            ! Wait for next beef
            WHILE b_A052_StartGrill=FALSE DO
                !
                ! Read beefer timer
                n_A052_CurrentBeefTime:=Round(ClkRead(clk_A052_BeefTime)\Dec:=2);
                !
                ! Check beef status 
                IF n_A052_CurrentBeefTime>n_A052_MaxBeefTime THEN
                    !
                    ! Beef killed
                    Stop;
                    !* SetDo doA052_Grill,0;
                    !* SetDo doA052_Kill,1;
                    !* PulseDO\High\PLength:=0.5,doA052_BeefUpdate;
                ENDIF
            ENDWHILE
            !
            ! Reset beefer timer
            ClkReset clk_A052_BeefTime;
            ClkStart clk_A052_BeefTime;
            !
            ! Select grill side
            IF b_A052_GrillSide1=TRUE THEN
                !
                ! Grill side one
                !
                ! Grill time 
                WaitTime n_A052_GrillTimeSide1;
            ELSEIF b_A052_GrillSide2=TRUE THEN
                !
                ! Grill side two
                !
                ! Grill time 
                WaitTime n_A052_GrillTimeSide2;
            ELSE
                !
                ! Program error
                TPErase;
                TPWrite "Program Error";
                TPWrite "No Grill Side";
                Stop\AllMoveTasks;
            ENDIF
            !
            ! Grill beef
            Stop;
            !* SetDO doA052_Grill,1;
            !* SetDO doA052_Kill,0;
            !* PulseDO\High\PLength:=0.5,doA052_BeefUpdate;
            !
            ! Grill time finish
            b_A052_StartGrill:=FALSE;
        ENDWHILE
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Inititialize cell 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.07.29
    ! **************** ETH Zürich *******************
    !
    PROC r_A052_InitCell()
        !
        ! Initialize signals
        r_A052_InitSig;
        !
        ! Initialize variables
        r_A052_InitVar;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Inititialize signals 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.07.29
    ! **************** ETH Zürich *******************
    !
    PROC r_A052_InitSig()
        !
        ! Reset Signals
        !
        ! Kill old Beef 
        Stop;
        !* SetDo doA052_Grill,0;
        !* SetDo doA052_Kill,1;
        !* PulseDO\High\PLength:=0.5,doA052_BeefUpdate;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Inititialize variables 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.07.29
    ! **************** ETH Zürich *******************
    !
    PROC r_A052_InitVar()
        !
        ! Reset variables
        b_A052_StartGrill:=FALSE;
        n_A052_CurrentBeefTime:=0;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

ENDMODULE