#pragma once


class CGameLogic
{
public:
	void Update(int t);

protected:
	void Move();
	void Talk();
	void Hit();
};

