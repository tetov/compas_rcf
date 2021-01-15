MODULE RFL_HMI_Ma
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
    ! Function    :     User Interface Window Home
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.08.11
    ! **************** ETH Zürich *******************
    !
    PROC r_RFL_UIMaWinHome()
        !
        ! View Window Home
        n_RFL_UiListItem:=UIListView(
                    \Result:=btn_RFL_Answer
                    \Header:="ETH Zürich / NCCR Digital Fabrication",
                    li_RFL_MaWinHome
                    \BtnArray:=st_RFL_BtnOkExit
                    \Icon:=iconInfo
                    \DefaultIndex:=1);
        !
        ! Check answer
        IF btn_RFL_Answer=1 THEN
            !
            ! Button answer OK
            TEST n_RFL_UiListItem
            CASE 1:
                !
                ! View Window ABB
                r_RFL_ProgError;
                r_RFL_UIMaWinABB;
            CASE 2:
                !
                ! View Window Project
                r_RFL_UIMaWinProject;
            CASE 3:
                !
                ! View Window System Helper 
                r_RFL_ProgError;
                st_RFL_JobFrmMa:="rRFL_SysHelper";
                !
                ! Master have a Job
                b_RFL_WaitForJob:=FALSE;
            CASE 4:
                !
                ! View Window Equipment & Tools
                r_RFL_ProgError;
            CASE 5:
                !
                ! Item Break Check
                r_RFL_ProgError;
                st_RFL_JobFrmMa:="rABB_MoveToBrakeCheckPos";
                !
                ! Master have a Job
                b_RFL_WaitForJob:=FALSE;
            DEFAULT:
                !
                ! Undefined Item 
                r_RFL_ProgError;
            ENDTEST
        ELSE
            !
            ! User has select Exit
        ENDIF
        !
        ! Start Job for Tasks
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     User Interface Window ABB
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2017.07.06
    ! **************** ETH Zürich *******************
    !
    PROC r_RFL_UIMaWinABB()
        !
        ! View Window ABB
        n_RFL_UiListItem:=UIListView(
                    \Result:=btn_RFL_Answer
                    \Header:="ABB",
                    li_RFL_MaWinABB
                    \BtnArray:=st_RFL_BtnOkExit
                    \Icon:=iconInfo
                    \DefaultIndex:=1);
        !
        ! Check answer
        IF btn_RFL_Answer=1 THEN
            !
            ! Button answer OK
            TEST n_RFL_UiListItem
            CASE 1:
                !
                ! Item ABB Example
                st_RFL_JobFrmMa:="rABB_Example";
            CASE 2:
                !
                ! Item ABB Calibration
                st_RFL_JobFrmMa:="rABB_CraneFunction";
            CASE 3:
                !
                ! Item ABB Calibration
                st_RFL_JobFrmMa:="rABB_MoveToCalibPos";
            DEFAULT:
                !
                ! Undefined Item 
                r_RFL_ProgError;
            ENDTEST
            !
            ! Master have a Job
            b_RFL_WaitForJob:=FALSE;
        ELSE
            !
            ! User has select Exit
        ENDIF
        !
        ! Start Job for Tasks
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     User Interface Window Project
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2017.07.06
    ! **************** ETH Zürich *******************
    !
    PROC r_RFL_UIMaWinProject()
        !
        ! View Window Project
        n_RFL_UiListItem:=UIListView(
                    \Result:=btn_RFL_Answer
                    \Header:="RFL Projects",
                    li_RFL_MaWinProject
                    \BtnArray:=st_RFL_BtnOkExit
                    \Icon:=iconInfo
                    \DefaultIndex:=1);
        !
        ! Check answer
        IF btn_RFL_Answer=1 THEN
            !
            ! Button answer OK
            TEST n_RFL_UiListItem
            CASE 1:
                !
                ! Item X000 Default 
                st_RFL_JobFrmMa:="r_A057_Main";
                st_RFL_CurMaJob:="A057";
            DEFAULT:
                !
                ! Undefined Item 
                r_RFL_ProgError;
            ENDTEST
            !
            ! Master have a Job
            b_RFL_WaitForJob:=FALSE;
            !
            ! Ask the user for a shortcut to his project
            n_RFL_Answer:=UIMessageBox(
                \Header:="RFL Projects"
                \MsgArray:=["If you want to set a shortcut to your project","select YES",""]
                \Buttons:=btnYesNo
                \Icon:=iconInfo);
            !
            ! Check the user answer
            IF n_RFL_Answer=resYes THEN
                !
                ! Yes
                ! Set the shortcut to the project;
                b_RFL_ProjectShortcut:=TRUE;
            ELSE
                !
                ! No
                ! Reset the shortcut to the project;
                b_RFL_ProjectShortcut:=FALSE;
            ENDIF
        ELSE
            !
            ! User has select Exit
        ENDIF
        !
        ! Start Job for Tasks
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

ENDMODULE