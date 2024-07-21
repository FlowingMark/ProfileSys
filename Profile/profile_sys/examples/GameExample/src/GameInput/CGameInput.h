#pragma once


class CGameInput
{
public:
	void Update(int t);

	void HandleKey();

	bool GameOver();

private:
	bool m_GameOver = false;
};

