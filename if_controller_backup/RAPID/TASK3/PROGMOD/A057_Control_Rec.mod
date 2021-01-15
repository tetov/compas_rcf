MODULE A057_Control_Rec
    !***********************************************************************************
    !
    ! ETH Zürich / Robotic Fabrication Lab
    ! HIB C 13 / Stefano-Franscini-Platz 1
    ! CH-8093 Zürich
    !
    !***********************************************************************************
    !
    ! PROJECT     :  A057 MAS Rio
    !
    ! FUNCTION    :  Main and Control Modul 
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2020.01.27
    !
    ! Copyright   :  ETH Zürich (CH) 2019
    !
    !***********************************************************************************

    !************************************************
    ! Function    :     Main function (start project) 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.11.29
    !***************** ETH Zürich *******************
    !
    PROC r_A057_Main()
        !
        ! Synchronize with master 
        WaitSyncTask id_A057_MainSta,tl_RFL_All;
        !
        ! Temp Msg for Operator
        TPWrite "A057 Main";
        !
        ! Initialize cell for Project
        r_A057_InitTask;
        !* r_A042_InitCell;
        !
        ! Production loop
        WHILE b_A057_Run=TRUE DO
            !
            ! Use RRC 
            r_A042_Main;
            !
        ENDWHILE
        !
        ! Message for Operator
        TPWrite st_RFL_Taskname+" in A057 End";
        ! 
        ! Synchronize with master 
        WaitSyncTask id_A057_MainEnd,tl_RFL_All;
        !
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Initialize cell for project
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.11.29
    ! **************** ETH Zürich *******************
    !
    PROC r_A057_InitTask()
        ! 
        WaitSyncTask id_A057_InitTaskSta,tl_RFL_All;
        !
        ! Speed
        r_A057_InitSpeed;
        !
        ! Signals
        r_A057_InitSig;
        !
        ! Variables
        r_A057_InitVar;
        !
        WaitSyncTask id_A057_InitTaskEnd,tl_RFL_All;
        ! 
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Initialize Signals for project
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.11.29
    ! **************** ETH Zürich *******************
    !
    PROC r_A057_InitSig()
        !
        WaitSyncTask id_A057_InitSigSta,tl_RFL_All;
        !
        !
        WaitSyncTask id_A057_InitSigEnd,tl_RFL_All;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Initialize variables for project
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.11.29
    !***************** ETH Zürich *******************
    !
    PROC r_A057_InitVar()
        ! 
        WaitSyncTask id_A057_InitVarSta,tl_RFL_All;
        ! 
        ! Placeholder
        !
        WaitSyncTask id_A057_InitVarEnd,tl_RFL_All;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Initialize speed settings for project
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.11.29
    !***************** ETH Zürich *******************
    !
    PROC r_A057_InitSpeed()
        !
        WaitSyncTask id_A057_InitSpeedSta,tl_RFL_All;
        !
        !
        WaitSyncTask id_A057_InitSpeedSet,tl_RFL_All;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC
ENDMODULE