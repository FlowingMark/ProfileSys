#pragma once


class CGameRender
{
public:
	void Render(int t);


protected:
	void RenderHead();

	void RenderBody();

	void RenderShadow();
};

