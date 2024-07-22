#include <iostream>
#include "../../../include/game_profile_sys_helper.h"
#include "GameInstance/CGameInstance.h"
int main()
{
	//game init
	CGameInstance GameInstance;
	GameInstance.InitGame();
	std::cout << "press \"ESC\" to exit !!" << std::endl;
	std::cout << "press \"s\" start record!!" << std::endl;
	std::cout << "press \"d\" end record!!" << std::endl;

	//game frame
	bool exit(false);
	while (!exit)
	{
		exit = GameInstance.RunFrame();
	}

	return 0;
}