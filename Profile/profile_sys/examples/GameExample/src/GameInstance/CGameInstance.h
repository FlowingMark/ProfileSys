#pragma once
#include <memory>

class CGameInput;
class CGameLogic;
class CGameRender;

class CGameInstance
{
public:
	CGameInstance();
	~CGameInstance();
	void InitGame();

	bool RunFrame();

protected:
	std::unique_ptr<CGameInput> m_GameInput;
	std::unique_ptr<CGameLogic> m_GameLogic;
	std::unique_ptr<CGameRender> m_GameRender;
};

