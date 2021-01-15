MODULE RFL_Helper_1
    !***********************************************************************************
    !
    ! ETH Zurich / NCCR Digital Fabrication
    ! HIP CO 11.1 / Gustave-Naville-Weg 1
    ! CH-8093 Zürich
    !
    !***********************************************************************************
    !
    ! PROJECT     :  A011_RFL
    !
    ! FUNCTION    :  Helper Routines for ETH
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2016.08.09 Draft
    !
    ! Copyright   :  ETH Zürich (CH) 2016
    !
    !***********************************************************************************

    !************************************************
    ! Function    :     Read curretn Roboterposition and write it in Temp Variables
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2017.05.05
    !***************** ETH Zürich *******************
    !
    PROC r_RFL_ReadPosTemp(\switch FlyBy)
        !
        ! Check for FlyBy
        IF Present(FlyBy) THEN
            !
            ! Do not wait for stand still
        ELSE
            !
            ! Wait for Robot in position or zero speed
            WaitRob\ZeroSpeed;
        ENDIF
        !
        ! Read current joint position
        jp_RFL_Temp:=CJointT();
        !
        ! Read current robtarget position
        p_RFL_Temp:=CRobT(\Tool:=tool0\WObj:=wobj0);
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Read curretn Robotertool and write it in Temp Variables
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2017.05.05
    !***************** ETH Zürich *******************
    !
    PROC r_RFL_ReadToolTemp()
        !
        ! Read tooldata and tool name
        GetSysData t_RFL_Temp\ObjectName:=st_RFL_TempToolName;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC
    
    !************************************************
    ! Function    :     Stor current position
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.11.16
    ! **************** ETH Zürich *******************
    !
    PROC r_RFL_StorePos()
        !
        ! Check that the robot is not in motion
        WaitRob\ZeroSpeed;
        !
        ! When robot in safepos z then not store
        IF f_RFL_CompJPos(jp_RFL_SafePosZ,1\bCheckZAxis:=TRUE\nLimMM:=1) THEN
            !
            ! Robot in SafePosZ => not stred
        ELSE
            ! Robot not in SafePosZ => stred
            !
            ! Store current position
            p_RFL_Store:=CRobT(\Tool:=tool0\WObj:=wobj0);
            !
            ! Store current jointvalues
            jp_RFL_Store:=CJointT();
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Current position
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.11.21
    ! **************** ETH Zürich *******************
    !
    PROC r_RFL_CurrentPos()
        !
        ! Check that the robot is not in motion
        WaitRob\ZeroSpeed;
        !
        ! Store current position
        p_RFL_Current:=CRobT(\Tool:=tool0\WObj:=wobj0);
        !
        ! Store current jointvalues
        jp_RFL_Current:=CJointT();
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Move back to stored position
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.11.16
    ! **************** ETH Zürich *******************
    !
    PROC r_RFL_RestorePos()
        VAR bool bConfJOff;
        !
        ! Read and store configuration state
        IF C_MOTSET.conf.jsup=FALSE bConfJOff:=TRUE;
        !
        ! Activate configuration
        ConfJ\On;
        !
        ! Move to stored position
        MoveJ p_RFL_Store,v_RFL_RestorPos,fine,tool0\WObj:=wobj0;
        !
        ! When the configuration was deactivated restor the state
        IF bConfJOff=TRUE ConfJ\Off;
        !
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     Test Relativ Task X-, Y-, Z-Axis 
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2016.11.17
    ! **************** ETH Zürich *******************
    ! Code example:
    ! IF fCheckAchsPos(jpRoStop,1) THEN
    !
    FUNC bool f_RFL_CompJPos(
        jointtarget jpCompare,
        num nLimDec,
        \bool bCheckXAxis,
        \bool bCheckYAxis,
        \bool bCheckZAxis,
        \num nLimMM)
        !
        ! Input Parameter:
        ! Jointarget to compare
        ! Limt [°] for comparability test
        ! opt. compare X-Axis
        ! opt. compare Y-Axis
        ! opt. compare Z-Axis
        ! Limt [mm] for comparability test
        !
        !  Return Parameter: 
        ! comparability test true or false
        VAR bool bRes:=TRUE;
        ! 
        ! Intern Declaration
        VAR jointtarget jpCurrent;
        !
        ! Start Function
        !
        ! Wait for Robo
        WaitRob\ZeroSpeed;
        !
        ! Read current jonttarget
        jpCurrent:=CJointT();
        !
        ! Compare Roboter Joints
        !
        ! If the values are too high, bRes go to "FALSE"
        IF Abs(jpCompare.robax.rax_1-jpCurrent.robax.rax_1)>=nLimDec bRes:=FALSE;
        IF Abs(jpCompare.robax.rax_2-jpCurrent.robax.rax_2)>=nLimDec bRes:=FALSE;
        IF Abs(jpCompare.robax.rax_3-jpCurrent.robax.rax_3)>=nLimDec bRes:=FALSE;
        IF Abs(jpCompare.robax.rax_4-jpCurrent.robax.rax_4)>=nLimDec bRes:=FALSE;
        IF Abs(jpCompare.robax.rax_5-jpCurrent.robax.rax_5)>=nLimDec bRes:=FALSE;
        IF Abs(jpCompare.robax.rax_6-jpCurrent.robax.rax_6)>=nLimDec bRes:=FALSE;
        !
        ! Compare X-Axis
        IF Present(bCheckXAxis) AND bCheckXAxis=TRUE THEN
            IF Abs(jpCompare.extax.eax_a-jpCurrent.extax.eax_a)>=nLimMM bRes:=FALSE;
        ENDIF
        !
        ! Compare Y-Axis
        IF Present(bCheckYAxis) AND bCheckYAxis=TRUE THEN
            IF Abs(jpCompare.extax.eax_b-jpCurrent.extax.eax_b)>=nLimMM bRes:=FALSE;
        ENDIF
        !
        ! Compare Z-Axis
        IF Present(bCheckZAxis) AND bCheckZAxis=TRUE THEN
            TPWrite ""\Num:=Abs(jpCompare.extax.eax_c-jpCurrent.extax.eax_c);
            IF Abs(jpCompare.extax.eax_c-jpCurrent.extax.eax_c)>=nLimMM bRes:=FALSE;
        ENDIF
        RETURN bRes;
    ENDFUNC
	PROC r_RFL_SysChangePos()
		MoveAbsJ [[6.47345E-07,-0.00132846,-0.000315338,-0.000474194,-0.00141919,0.00235598],[21577.5,-2428.39,-4515,0,0,0]]\NoEOffs, v1000, z50, tool0;
	ENDPROC

    !************************************************
    ! Function    :     TP Message User Information
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2017.05.19
    ! **************** ETH Zürich *******************
    !
    PROC r_RFL_TPMsg(string stMsg)
        ! 
        ! Clear Msg Panel
        TPErase;
        !
        ! Msg for user
        TPWrite stMsg;
        !
        ! Time to read the Msg
        WaitTime n_RFL_TimeTPMsg;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC

    !************************************************
    ! Function    :     User Information
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.06
    ! **************** ETH Zürich *******************
    !
    PROC r_RFL_UIMsg(string stMsgHeader,string stMsgL1,\string stMsgL2,\string stMsgL3,\string stMsgL4,\string stMsgL5,icondata icIcon)
        VAR string stMsg{5}:=["","","","",""];
        !
        ! Clear message 
        stMsg:=["","","","",""];
        !
        ! Load meassge 
        stMsg{1}:=stMsgL1;
        IF Present(stMsgL2) stMsg{2}:=stMsgL2;
        IF Present(stMsgL3) stMsg{3}:=stMsgL3;
        IF Present(stMsgL4) stMsg{4}:=stMsgL4;
        IF Present(stMsgL5) stMsg{5}:=stMsgL5;
        !
        ! Msg for user
        n_RFL_Answer:=UIMessageBox(
            \Header:=stMsgHeader
            \MsgArray:=stMsg
            \BtnArray:=["Ignor"]
            \Icon:=icIcon);
    ERROR
        ! Placeholder for Error Code...
    ENDPROC
    
    !************************************************
    ! Function    :     Log Message User Information
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2017.04.26
    ! **************** ETH Zürich *******************
    !
    PROC r_RFL_LogMsg(string stHeader,string stMsg)
        ! 
        ! Msg for user
        ErrWrite \I, stHeader+" "+stMsg,"rLogMsg";
    ERROR
        ! Placeholder for Error Code...
    ENDPROC
    
    !************************************************
    ! Function    :     Check Y-Axis collision for moving
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2017.05.19
    !***************** ETH Zürich *******************
    !
    PROC r_RFL_CheckYAxisCol(robtarget pCheck)
        VAR num nY21;
        VAR num nY22;
        VAR num nMinDistance;
        VAR num nSafeOffs;
        !
        ! Set Default Values
        nSafeOffs:=40;
        nMinDistance:=-2587-nSafeOffs;
        !
        ! Read current pos form Rob11
        p_RFL_Temp:=CRobT(\TaskName:="T_Rob22"\Tool:=tool0\WObj:=wobj0);
        !
        ! Write axis values to variable
        nY21:=pCheck.extax.eax_b;
        nY22:=p_RFL_Temp.extax.eax_b-nMinDistance;
        !
        ! Compaire the Y-Values
        IF nY21>nY22 THEN
            !
            ! No collision
        ELSE
            !
            ! Y-Axis will collide
            r_RFL_TPMsg " Y-Axis Collision";
            TPWrite "Max. Y-Position    = "\Num:=nY22;
            TPWrite "Planned Y-Position = "\Num:=nY21;
            !
            ! Stop program
            Stop;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC
    
    !************************************************
    ! Function    :     Go to calibration position
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.10.18
    !***************** ETH Zürich *******************
    !
    PROC r_RFL_GoToCalib()
        !
        ! Move to calibration position
        MoveAbsJ jp_RFL_CalibPos\NoEOffs,v200,fine,tool0\WObj:=wobj0;
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC
ENDMODULE