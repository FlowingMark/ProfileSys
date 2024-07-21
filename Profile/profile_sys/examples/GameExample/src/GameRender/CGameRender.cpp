#include "CGameRender.h"
#include <iostream>
#include <Windows.h>

void CGameRender::Render(int t)
{
	std::cout << __FUNCTION__ << std::endl;
	RenderHead();
	RenderBody();
	RenderShadow();
}

void CGameRender::RenderHead()
{
	std::cout << __FUNCTION__ << std::endl;
	Sleep(rand()%1000);
}

void CGameRender::RenderBody()
{
	std::cout << __FUNCTION__ << std::endl;
	Sleep(rand()%2000);
}

void CGameRender::RenderShadow()
{
	std::cout << __FUNCTION__ << std::endl;
	Sleep(rand()%3000);
}
