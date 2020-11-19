MODULE RFL_Control_Sen
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
    ! HISTORY     :  2019.11.28 Draft
    !
    ! Copyright   :  ETH Zürich (CH) 2016
    !
    !***********************************************************************************

    !************************************************
    ! Function    :     Function of the Routine
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2017.05.05
    !***************** ETH Zürich *******************
    !
    PROC main()
        !
        ! wait until master has set taskliste all
        WaitTime n_RFL_TimeTaskLiAll;
        !
        ! Inititialize Task
        r_RFL_InitTask;
        !
        ! Work process
        WHILE b_RFL_Run=TRUE DO
            !
            ! Idle Loop
            WHILE b_RFL_WaitForJob DO
                !
                ! User Interface
                ! 
                ! Short waittime
                WaitTime 0.1;
            ENDWHILE
            !
            ! Execute  Job from Master
            r_RFL_ExecuteJobFrmMa;
        ENDWHILE
        RETURN ;
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
        ! Add here code..
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
        ! Add here code..
        !
        WaitSyncTask id_RFL_InitSpeedSet,tl_RFL_All;
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
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

ENDMODULE