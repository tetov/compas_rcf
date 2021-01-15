MODULE RFL_Control_Ma
    !***********************************************************************************
    !
    ! ETH Zürich / Robotic Fabrication Lab
    ! HIB C 13 / Stefano-Franscini-Platz 1
    ! CH-8093 Zürich
    !
    !***********************************************************************************
    !
    ! PROJECT     :  A011_RFL
    !
    ! FUNCTION    :  Control Routines for ETH
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2016.08.11 Draft
    !
    ! Copyright   :  ETH Zürich (CH) 2016
    !
    !***********************************************************************************

    !************************************************
    ! Function    :     Main
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.11
    ! **************** ETH Zürich *******************
    !
    PROC main()
        !
        ! Read system specification
        r_RFL_SysSpec;
        !
        ! Initalisation 
        r_RFL_InitTask;
        !
        ! Work process
        WHILE b_RFL_Run=TRUE DO
            !
            ! Idle Loop
            WHILE b_RFL_WaitForJob=TRUE DO
                !
                ! User Interface
                r_RFL_UIMaWinHome;
                ! 
                ! Short waittime
                WaitTime 0.1;
            ENDWHILE
            !
            ! Execute  Job from Master
            r_RFL_ExecuteJobFrmMa;
        ENDWHILE
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Initialize Task
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.11
    ! **************** ETH Zürich *******************
    !
    PROC r_RFL_InitTask()
        ! 
        WaitSyncTask id_RFL_InitTaskSta,tl_RFL_All;
        !
        ! Clear TP Window
        TPErase;
        !
        ! Speed
        r_RFL_InitSpeed;
        !
        ! Signals
        r_RFL_InitSig;
        !
        ! Variables
        r_RFL_InitVar;
        !
        WaitSyncTask id_RFL_InitTaskEnd,tl_RFL_All;
        ! 
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Initialize Signals
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2017.09.27
    ! **************** ETH Zürich *******************
    !
    PROC r_RFL_InitSig()
        !
        WaitSyncTask id_RFL_InitSigSta,tl_RFL_All;
        !
        !
        WaitSyncTask id_RFL_InitSigEnd,tl_RFL_All;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Initialize Variables
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.11
    ! **************** ETH Zürich *******************
    !
    PROC r_RFL_InitVar()
        !
        WaitSyncTask id_RFL_InitVarSta,tl_RFL_All;
        !
        ! Read Task Name
        st_RFL_Taskname:=GetTaskName();
        !
        ! Set master zone data
        z_RFL_MaMin:=z10;
        z_RFL_MaMed:=z100;
        z_RFL_MaMax:=z200;
        !
        ! FlexPendant porgrammable key 4 is used for Master reset
        IF doMaFP3=1 OR b_RFL_ProjectShortcut=FALSE THEN
            !
            ! Master reset
            !
            ! Reset the project shortcut to start the Masterwindow
            b_RFL_ProjectShortcut:=FALSE;
            !
            ! Reset job for master
            b_RFL_WaitForJob:=TRUE;
            st_RFL_JobFrmMa:="InitVar";
            st_RFL_CurMaJob:="InitVar";
            !
            ! Reset the resetsignal 
            SetDo doMaFP3,0;
        ELSE
            !
            ! No master reset
        ENDIF
        !
        WaitSyncTask id_RFL_InitVarEnd,tl_RFL_All;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Initialize Speed
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2018.02.21
    ! **************** ETH Zürich *******************
    !
    PROC r_RFL_InitSpeed()
        ! 
        WaitSyncTask id_RFL_InitSpeedSta,tl_RFL_All;
        !
        ! Speed limit off
        r_RFL_SpeedLimitOff;
        !
        ! Wait until speed is set in task
        WaitSyncTask id_RFL_InitSpeedSet,tl_RFL_All;
        !
        ! Speed limit on
        r_RFL_SpeedLimitOn;
        ! 
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Execute Job from Master
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.11
    ! **************** ETH Zürich *******************
    !
    PROC r_RFL_ExecuteJobFrmMa()
        !
        WaitSyncTask id_RFL_ExeJobFrmMaSta,tl_RFL_All;
        !
        %st_RFL_JobFrmMa %;
        !
        WaitSyncTask id_RFL_ExeJobFrmMaEnd,tl_RFL_All;
        ! 
        ! Job finish
        b_RFL_WaitForJob:=TRUE;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     ProgError
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.11
    ! **************** ETH Zürich *******************
    !
    PROC r_RFL_ProgError()
        ! 
        ! User Msg
        r_RFL_TPMsg "Program Error or not finisht programmed";
        !
        ! Stop Program
        Stop;
        Stop;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

ENDMODULE