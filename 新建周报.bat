@echo off
chcp 65001 >nul
title 大秦无人机周报生成器

echo ============================================================
echo    大秦无人机低空周报 - 生成器
echo ============================================================
echo.
echo  请选择生成模式：
echo.
echo    [1] 全自动模式 - 自动搜集内容生成完整周报
echo    [2] 框架模式 - 仅生成HTML框架（后续手动填内容）
echo    [3] 退出
echo.
set /p choice=请输入选项 (1/2/3): 

if "%choice%"=="1" goto auto
if "%choice%"=="2" goto framework
if "%choice%"=="3" goto end
goto invalid

:auto
echo.
echo ============================================================
echo    正在启动：全自动生成模式
echo ============================================================
python generate_weekly_auto.py
pause
goto end

:framework
echo.
echo ============================================================
echo    正在启动：框架生成模式
echo ============================================================
python generate_weekly.py
pause
goto end

:invalid
echo.
echo 无效选项，请重新运行
pause

:end
