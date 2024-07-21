#include "CGameLogic.h"
#include <iostream>
#include <Windows.h>

void CGameLogic::Update(int t)
{
	std::cout << __FUNCTION__ << std::endl;
	Move();
	Talk();
	Hit();
}

void CGameLogic::Move()
{
	std::cout << __FUNCTION__ << std::endl;
	Sleep(rand()%200);
}

void CGameLogic::Talk()
{
	std::cout << __FUNCTION__ << std::endl;
	Sleep(rand()%200);
}

void CGameLogic::Hit()
{
	std::cout << __FUNCTION__ << std::endl;
	Sleep(rand()%1000);
}
