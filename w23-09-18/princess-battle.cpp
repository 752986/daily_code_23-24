#include <string>
#include <cstdio>
using namespace std;

enum class DefendResult {
	Blocked,
	Softened,
	Taken
};

class Princess {
private:
	string name;
	int healthPoints;
	int attackPoints;
	int defensePoints;
	int magicPoints;
public:
	Princess(string name, int hp, int ap, int dp, int mp) {
		this->name = name;
		healthPoints = hp;
		attackPoints = ap;
		defensePoints = dp;
		magicPoints = mp;
	}

	int attack() {
		return rand() % attackPoints;
	}

	DefendResult defend(int incomingAttack) {
		int roll = rand() % 10;
		if (defensePoints > roll + 2) {
			return DefendResult::Blocked;
		} else if (defensePoints > roll) {
			healthPoints -= incomingAttack / 2;
			return DefendResult::Softened;
		} else {
			healthPoints -= incomingAttack;
			return DefendResult::Taken;
		}
	}

	string getName() { return name; }

	int getHealth() { return healthPoints; }
};

int main() {
	Princess pocohontos("Pocahontas", 50, 9, 4, 1000);
	Princess miku("Hatsune Miku", 40, 14, 5, 2);

	printf("%s vs. %s\n\n", pocohontos.getName().c_str(), miku.getName().c_str());

	while (pocohontos.getHealth() > 0 and miku.getHealth() > 0) {
		int attack1 = pocohontos.attack();
		if (attack1 == 0) {
			printf("%s fumbled the attack!\n", pocohontos.getName().c_str());
		} else {
			printf("%s attacks for %d\n", pocohontos.getName().c_str(), attack1);
		}
		DefendResult defend1 = miku.defend(attack1);
		switch (defend1) {
			case DefendResult::Blocked:
				printf("%s blocked the attack\n", miku.getName().c_str());
				break;
			case DefendResult::Softened:
				printf("%s took reduced damage. Thay have %d health left.\n", miku.getName().c_str(), miku.getHealth());
				break;
			case DefendResult::Taken:
				printf("%s took damage. Thay have %d health left.\n", miku.getName().c_str(), miku.getHealth());
				break;
		}

		int attack2 = miku.attack();
		if (attack2 == 0) {
			printf("%s fumbled the attack!\n", miku.getName().c_str());
		} else {
			printf("%s attacks for %d\n", miku.getName().c_str(), attack2);
		}
		DefendResult defend2 = pocohontos.defend(attack2);
		switch (defend2) {
			case DefendResult::Blocked:
				printf("%s blocked the attack\n", pocohontos.getName().c_str());
				break;
			case DefendResult::Softened:
				printf("%s took reduced damage. Thay have %d health left.\n", pocohontos.getName().c_str(), pocohontos.getHealth());
				break;
			case DefendResult::Taken:
				printf("%s took damage. Thay have %d health left.\n", pocohontos.getName().c_str(), pocohontos.getHealth());
				break;
		}

		system("pause");
		printf("\n");
	}
}