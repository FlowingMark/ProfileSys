#include "CGameInput.h"
#include <iostream>
#include <conio.h>
#include <Windows.h>
#include "../../../../include/game_profile_sys_helper.h"

void CGameInput::Update(int t)
{
	int randNum = rand() % 1000;
	Sleep(randNum);
	std::cout << __FUNCTION__ << std::endl;
}

void CGameInput::HandleKey()
{
	int ch;
	if (_kbhit())
	{
		ch = _getch();
		std::cout << ch;
		if (ch == 27)// ESC == 27
		{
			std::cout << "game over!!" << std::endl;
			m_GameOver = true;
		}
		else if (ch == 115)// s == 115
		{
			if (g_profile_sys)
			{
				g_profile_sys->start();
			}
		}
		else if (ch == 100)// d == 100
		{
			if (g_profile_sys)
			{
				g_profile_sys->dump2File(time(nullptr));
			}
		}
		else
		{
			std::cout << ch << std::endl;
		}
	}
}

bool CGameInput::GameOver()
{
	return m_GameOver;
}
