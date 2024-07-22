#include "CGameInstance.h"
#include "../GameInput/CGameInput.h"
#include "../GameLogic/CGameLogic.h"
#include "../GameRender/CGameRender.h"
#include "../../../../include/game_profile_sys_helper.h"


CGameInstance::CGameInstance()
{
}

CGameInstance::~CGameInstance()
{
}

void CGameInstance::InitGame()
{
	m_GameInput.reset(new CGameInput());
	m_GameLogic.reset(new CGameLogic());
	m_GameRender.reset(new CGameRender());
}

bool CGameInstance::RunFrame()
{CGameProFile(-1)
	m_GameInput->HandleKey();
	if (m_GameInput->GameOver())
		return true;
	m_GameInput->Update(1);

	m_GameLogic->Update(1);

	m_GameRender->Render(1);

	return false;
}
