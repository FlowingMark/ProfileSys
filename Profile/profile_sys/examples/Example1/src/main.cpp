#include <iostream>
#include "../../../include/game_profile_sys_helper.h"
int main()
{
	//only for load dll
	CGameProFile(-22);
	//start record
	if (g_profile_sys)
	{
		g_profile_sys->start();
	}
	
	{
		CGameProFile(-1)

		{
			CGameProFile(2)
				std::cout << "hello world 2" << std::endl;

			Sleep(1000);
			CGameProFileUser(3)
				std::cout << "hello world 3" << std::endl;
			Sleep(2000);
			Sleep(1000);
			CGameProFileUser(4)
				std::cout << "hello world 4" << std::endl;
			Sleep(2000);
			{
				CGameProFile(5)
				for (int i = 0; i < 20; i++)
				{
					CGameProFile(6);
					Sleep(200);
				}
			}

		}
	}

	//end record
	if (g_profile_sys)
	{
		g_profile_sys->dump2File(123);
	}

	return 0;
}