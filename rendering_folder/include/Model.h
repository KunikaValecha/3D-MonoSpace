#pragma once

#include <vector>
#include <string>

#include <assimp/Importer.hpp>
#include <assimp/scene.h>
#include <assimp/postprocess.h>
#include <assimp/cimport.h>
#include <assimp/config.h>

#include <glm/glm.hpp>

#include "Mesh.h"
#include "Texture.h"

class Model
{
public:

	float depth, xPos, yPos;
	float rotX, rotY, rotZ;
	float scaleX, scaleY, scaleZ;
	float zSize, xSize, ySize;
	glm::vec3 colour;

	Model();
	Model(float d, float x, float y);
	void SetScale(float x,float y, float z);

	void LoadModel(const std::string& fileName);
	void RenderModel();
	void ClearModel();

	~Model();

private:

	void LoadNode(aiNode *node, const aiScene *scene);
	void LoadMesh(aiMesh *mesh, const aiScene *scene);
	void LoadMaterials(const aiScene *scene);

	std::vector<Mesh*> meshList;
	std::vector<Texture*> textureList;
	std::vector<unsigned int> meshToTex;
};

