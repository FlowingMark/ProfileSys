#include "CGameInput.h"
#include <iostream>
#include <conio.h>
#include <Windows.h>

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
