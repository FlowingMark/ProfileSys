#pragma once
#include "game_profile_sys.h"
#include <chrono>
#include <Windows.h>

using ProfileSysFunc = IGameProfileSys * (*)();

__declspec(selectany) IGameProfileSys* g_profile_sys = nullptr;

class CGameProfileSysTrigger
{
public:
	CGameProfileSysTrigger(int func_id)
	{
		static int initProfileSysOnce = loadProfileSysMod("profile_sys.dll");
		if (g_profile_sys)
		{
			m_func_index = func_id;
			m_start = std::chrono::system_clock::now();
			m_start_index = g_profile_sys->getCurIndex();
		}
	}
	~CGameProfileSysTrigger()
	{
		if (g_profile_sys)
		{
			auto end = std::chrono::system_clock::now();
			std::chrono::microseconds duration = std::chrono::duration_cast<std::chrono::microseconds>(end - m_start);
			g_profile_sys->addCallProfile(m_func_index, int(duration.count()), m_start_index);
		}
	}

	int loadProfileSysMod(const char* filename)
	{
		auto m_handle = LoadLibraryA(filename);
		if (!m_handle)
		{
			auto err = GetLastError();
		}
		else
		{
			auto func = (ProfileSysFunc)GetProcAddress(m_handle, "GetProfileSys");
			if (func)
			{
				g_profile_sys = func();
			}
		}
		return 1;
	}

protected:
	std::chrono::system_clock::time_point m_start;
	int m_func_index = 0;
	int m_start_index = 0;
};


#define CGameProFile(func_id) CGameProfileSysTrigger proFile007(func_id);
#define CGameProFileUser(func_id) CGameProfileSysTrigger proFile007##func_id(func_id);

