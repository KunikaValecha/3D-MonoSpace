#include "../include/Scene.h"

static const char* vShader = "shaders/shader.vert";
static const char* fShader = "shaders/shader.frag";
const float toRadians = 3.14159265f / 180.0f;

using namespace std;

Scene::Scene()
{
    uniformProjection = 0; 
    uniformModel = 0; 
    uniformView = 0; 
    uniformEyePosition = 0; 
    uniformSpecularIntensity = 0; 
    uniformShininess = 0; 
    uniformFogColour = 0;
	uniformDirectionalLightTransform = 0; 
	uniformOmniLightPos = 0;
	uniformFarPlane = 0;

    pointLightCount = 0; spotLightCount = 0;

    deltaTime = 0.0f;
    lastTime = 0.0f;
}

Scene::Scene(char* fileName)
{
	uniformProjection = 0; 
    uniformModel = 0; 
    uniformView = 0; 
    uniformEyePosition = 0; 
    uniformSpecularIntensity = 0; 
    uniformShininess = 0; 
    uniformFogColour = 0;
	uniformDirectionalLightTransform = 0; 
	uniformOmniLightPos = 0;
	uniformFarPlane = 0;

    pointLightCount = 0; spotLightCount = 0;

    deltaTime = 0.0f;
    lastTime = 0.0f;
    InitFromFile(fileName);
}

void Scene::calcAverageNormals(unsigned int * indices, unsigned int indiceCount, GLfloat * vertices, unsigned int verticeCount, 
						unsigned int vLength, unsigned int normalOffset)
{
	for (size_t i = 0; i < indiceCount; i += 3)
	{
		unsigned int in0 = indices[i] * vLength;
		unsigned int in1 = indices[i + 1] * vLength;
		unsigned int in2 = indices[i + 2] * vLength;
		glm::vec3 v1(vertices[in1] - vertices[in0], vertices[in1 + 1] - vertices[in0 + 1], vertices[in1 + 2] - vertices[in0 + 2]);
		glm::vec3 v2(vertices[in2] - vertices[in0], vertices[in2 + 1] - vertices[in0 + 1], vertices[in2 + 2] - vertices[in0 + 2]);
		glm::vec3 normal = glm::cross(v1, v2);
		normal = glm::normalize(normal);
		
		in0 += normalOffset; in1 += normalOffset; in2 += normalOffset;
		vertices[in0] += normal.x; vertices[in0 + 1] += normal.y; vertices[in0 + 2] += normal.z;
		vertices[in1] += normal.x; vertices[in1 + 1] += normal.y; vertices[in1 + 2] += normal.z;
		vertices[in2] += normal.x; vertices[in2 + 1] += normal.y; vertices[in2 + 2] += normal.z;
	}

	for (size_t i = 0; i < verticeCount / vLength; i++)
	{
		unsigned int nOffset = i * vLength + normalOffset;
		glm::vec3 vec(vertices[nOffset], vertices[nOffset + 1], vertices[nOffset + 2]);
		vec = glm::normalize(vec);
		vertices[nOffset] = vec.x; vertices[nOffset + 1] = vec.y; vertices[nOffset + 2] = vec.z;
	}
}

void Scene::CreateObjects() 
{
	unsigned int floorIndices[] = {
		0, 2, 1,
		1, 2, 3
	};

	GLfloat floorVertices[] = {
		-1000.0f, 0.0f, -1000.0f, 0.0f, 0.0f,	0.0f, -1.0f, 0.0f,
		 1000.0f, 0.0f, -1000.0f, 1.0f, 0.0f,	0.0f, -1.0f, 0.0f,
		-1000.0f, 0.0f,  1000.0f, 0.0f, 1.0f,	0.0f, -1.0f, 0.0f,
		 1000.0f, 0.0f,  1000.0f, 1.0f, 1.0f,	0.0f, -1.0f, 0.0f
	};

	unsigned int backWallIndices[] = {
		0, 2, 1,
		1, 2, 3
	};

	GLfloat backWallVertices[] = {
		-100.0f,   0.0f, -100.0f, 0.0f, 0.0f,	0.0f, 0.0f, -1.0f,
		 100.0f,   0.0f, -100.0f, 1.0f, 0.0f,	0.0f, 0.0f, -1.0f,
		-100.0f, 100.0f, -100.0f, 0.0f, 1.0f,	0.0f, 0.0f, -1.0f,
		 100.0f, 100.0f, -100.0f, 1.0f, 1.0f,	0.0f, 0.0f, -1.0f
	};

	Mesh *floor = new Mesh();
	floor->CreateMesh(floorVertices, floorIndices, 32, 6);
	meshList.push_back(floor);

	Mesh* wall = new Mesh();
	wall->CreateMesh(backWallVertices, backWallIndices, 32, 6);
	meshList.push_back(wall);
}

// void Scene::TransformAndRenderModel(Model* m, Material* mat, GLfloat transX, GLfloat transY, GLfloat transZ, GLfloat scale, GLfloat rotX, GLfloat rotY, GLfloat rotZ)
// {
// 	// First translate, rotate, then scale so that it's executed as scale, rotate, translate
// 	glm::mat4 model = glm::mat4();
// 	model = glm::translate(model, glm::vec3(transX, transY, transZ));
// 	model = glm::rotate(model, toRadians * rotX, glm::vec3(1, 0, 0));
// 	model = glm::rotate(model, toRadians * rotY, glm::vec3(0, 1, 0));
// 	model = glm::rotate(model, toRadians * rotZ, glm::vec3(0, 0, 1));
// 	model = glm::scale(model, glm::vec3(scale, scale, scale));
// 	glUniformMatrix4fv(uniformModel, 1, GL_FALSE, glm::value_ptr(model));
// 	mat->UseMaterial(uniformSpecularIntensity, uniformShininess);
// 	m->RenderModel();
// }

void Scene::TransformAndRenderModel(Model* m, Material* mat, GLfloat transX, GLfloat transY, GLfloat transZ, GLfloat scaleX, GLfloat scaleY, GLfloat scaleZ, GLfloat rotX, GLfloat rotY, GLfloat rotZ)
{
	glm::mat4 model = glm::mat4();
    model = glm::translate(model, glm::vec3(transX, transY, transZ));
 //    float sinHalfAngle = sin(rotY / 2);
	// float cosHalfAngle = cos(rotY / 2);

	// float rX = transX*sinHalfAngle;
	// float rY = transY*sinHalfAngle;
	// float rZ = transZ*sinHalfAngle;
	// float rW = cosHalfAngle;

	// glm::quat rota(rX, rY, rZ, rW);

	// glm::mat4 rotation = glm::mat4_cast(rota)*rotation;
	// model = rotation*model;
	
 	model = glm::rotate(model,  toRadians * rotX, glm::vec3(1, 0, 0));
	
	// // model = glm::translate(model, glm::vec3(transX, transY, transZ));
	
	model = glm::rotate(model, toRadians * rotY, glm::vec3(0, 1, 0));
	model = glm::rotate(model,  toRadians * rotZ, glm::vec3(0, 0, 1));
	model = glm::scale(model, glm::vec3(scaleX, scaleY, scaleZ));
	// model = modelx * modely + modelz;
	// model = glm::translate(model, glm::vec3(transX, transY, transZ));

	
	// model = glm::translate(model, -glm::vec3(transX, transY, transZ));
	
	glUniformMatrix4fv(uniformModel, 1, GL_FALSE, glm::value_ptr(model));
	mat->UseMaterial(uniformSpecularIntensity, uniformShininess);
	glUniform3f(uniformColour, m->colour.x, m->colour.y, m->colour.z);
	m->RenderModel();
}

void Scene::TransformAndRenderMesh(Mesh* m, Material* mat, GLfloat transX, GLfloat transY, GLfloat transZ, GLfloat scale, GLfloat rotX, GLfloat rotY, GLfloat rotZ)
{
	glm::mat4 model = glm::mat4();
	model = glm::translate(model, glm::vec3(transX, transY, transZ));
	// float sinHalfAngle = sin(rotY / 2);
	// float cosHalfAngle = cos(rotY / 2);

	// float rX = transX*sinHalfAngle;
	// float rY = transY*sinHalfAngle;
	// float rZ = transZ*sinHalfAngle;
	// float rW = cosHalfAngle;

	// glm::quat rota(rX, rY, rZ, rW);

	// glm::mat4 rotation = glm::mat4_cast(rota)*rotation;
	
	// glm::mat4 modelx = glm::rotate(model,  toRadians * rotX , glm::vec3(1, 0, 0));
	
	// glm::mat4 modely = glm::rotate(model,  toRadians * rotY , glm::vec3(0, 1, 0));
	// glm::mat4 modelz = glm::rotate(model, toRadians * rotZ, glm::vec3(0, 0, 1));
	// model = modelx * modely * modelz;
	
	model= glm::rotate(model,  toRadians * rotX , glm::vec3(1, 0, 0));
	
	model = glm::rotate(model,  toRadians * rotY , glm::vec3(0, 1, 0));
	model = glm::rotate(model, toRadians * rotZ, glm::vec3(0, 0, 1));
	model = glm::scale(model, glm::vec3(scale, scale, scale));
	// model = rotation*model;


	glUniformMatrix4fv(uniformModel, 1, GL_FALSE, glm::value_ptr(model));

	plainTexture.UseTexture();
	//glUniform3f(uniformColour, 1.0f, 1.0f, 1.0f);
	mat->UseMaterial(uniformSpecularIntensity, uniformShininess);
	m->RenderMesh();
}

void Scene::CreateShaders()
{
	Shader *shader1 = new Shader();
	shader1->CreateFromFiles(vShader, fShader);
	shaderList.push_back(*shader1);
	directionalShadowShader.CreateFromFiles("shaders/directionalShadowMap.vert", "shaders/directionalShadowMap.frag");
	omniShadowShader.CreateFromFiles("shaders/omniShadowMap.vert", "shaders/omniShadowMap.frag", "shaders/omniShadowMap.geom");

}

void Scene::RenderScene()
{
	glm::mat4 model;	
	TransformAndRenderMesh(meshList[0], &dullMaterial, 0.0f, 0.0f, 0.0f, 1.0f, 0.0f, 0.0f, 0.0f);

	for(size_t i = 0; i < modelList.size(); i++)
	{
		TransformAndRenderModel(&modelList[i], &dullMaterial, modelList[i].xPos, modelList[i].yPos, modelList[i].depth, modelList[i].scaleX, modelList[i].scaleY, modelList[i].scaleZ, modelList[i].rotX, modelList[i].rotY, modelList[i].rotZ);
	}
	
}

void Scene::OmniShadowMapPass(PointLight* light)
{
	directionalShadowShader.UseShader();

	glViewport(0, 0, mainLight.GetShadowMap()->GetShadowWidth(), mainLight.GetShadowMap()->GetShadowHeight());

	light->GetShadowMap()->Write();
	glClear(GL_DEPTH_BUFFER_BIT);

	uniformModel = omniShadowShader.GetModelLocation();
	uniformOmniLightPos = omniShadowShader.GetOmniLightPos();
	uniformFarPlane = omniShadowShader.GetFarPlane();

	glUniform3f(uniformOmniLightPos, light->GetPosition().x, light->GetPosition().y, light->GetPosition().z);
	glUniform1f(uniformFarPlane, light->GetFarPlane());
	std::vector<glm::mat4> temp = light->CalculateLightTransform();
	omniShadowShader.SetOmniLightMatrices(temp);

	omniShadowShader.Validate();

	RenderScene();

	glBindFramebuffer(GL_FRAMEBUFFER, 0);
}


void Scene::DirectionalShadowMapPass()
{
	directionalShadowShader.UseShader();

	glViewport(0, 0, mainLight.GetShadowMap()->GetShadowWidth(), mainLight.GetShadowMap()->GetShadowHeight());

	mainLight.GetShadowMap()->Write();
	glClear(GL_DEPTH_BUFFER_BIT);

	uniformModel = directionalShadowShader.GetModelLocation();
	glm::mat4 temp = mainLight.CalculateLightTransform();
	directionalShadowShader.SetDirectionalLightTransform(&temp);

	directionalShadowShader.Validate();

	RenderScene();

	glBindFramebuffer(GL_FRAMEBUFFER, 0);
}

void Scene::RenderPass(glm::mat4 viewMatrix)
{
	shaderList[0].UseShader();

	uniformModel = shaderList[0].GetModelLocation();
	uniformProjection = shaderList[0].GetProjectionLocation();
	uniformView = shaderList[0].GetViewLocation();
	uniformModel = shaderList[0].GetModelLocation();
	uniformEyePosition = shaderList[0].GetEyePositionLocation();
	uniformSpecularIntensity = shaderList[0].GetSpecularIntensityLocation();
	uniformShininess = shaderList[0].GetShininessLocation();
	uniformFogColour = shaderList[0].GetFogColourLocation();

	glViewport(0, 0, mainWindow.getWidth(), mainWindow.getHeight());

	glClearColor(0.9f, 1.0f, 1.0f, 1.0f);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	glUniformMatrix4fv(uniformProjection, 1, GL_FALSE, glm::value_ptr(projection));
	glUniformMatrix4fv(uniformView, 1, GL_FALSE, glm::value_ptr(viewMatrix));
	glUniform3f(uniformEyePosition, camera.getCameraPosition().x, camera.getCameraPosition().y, camera.getCameraPosition().z);
	glUniform4f(uniformFogColour, 0.4f, 0.4f, 0.4f, 1.0f);

	shaderList[0].SetDirectionalLight(&mainLight);
	shaderList[0].SetPointLights(pointLights, pointLightCount, 3, 0);
	shaderList[0].SetSpotLights(spotLights, spotLightCount, 3 + pointLightCount, pointLightCount);
	glm::mat4 temp = mainLight.CalculateLightTransform();
	shaderList[0].SetDirectionalLightTransform(&temp);

	mainLight.GetShadowMap()->Read(GL_TEXTURE2);
	shaderList[0].SetTexture(1);
	shaderList[0].SetDirectionalShadowMap(2);

	glm::vec3 lowerLight = camera.getCameraPosition();
	lowerLight.y -= 0.3f;
	spotLights[0].SetFlash(lowerLight, camera.getCameraDirection());

	shaderList[0].Validate();

	RenderScene();
}

void Scene::Render()
{
	GLfloat now = glfwGetTime(); // SDL_GetPerformanceCounter();
	deltaTime = now - lastTime; // (now - lastTime)*1000/SDL_GetPerformanceFrequency();
	lastTime = now;


	// Get + Handle User Input
	glfwPollEvents();

	camera.keyControl(mainWindow.getsKeys(), deltaTime);
	camera.mouseControl(mainWindow.getXChange(), mainWindow.getYChange());

	DirectionalShadowMapPass();

	for(size_t i = 0; i < pointLightCount; i++)
	{
		OmniShadowMapPass(&pointLights[i]);
	}

	for(size_t i = 0; i < spotLightCount; i++)
	{
		OmniShadowMapPass(&spotLights[i]);
	}
	
	RenderPass(camera.calculateViewMatrix());

	mainWindow.swapBuffers();
}

void Scene::InitFromFile(char* fileName)
{
	mainWindow = Window(1242, 375);
	mainWindow.Initialise();

	CreateObjects();
	CreateShaders();

	camera = Camera(glm::vec3(0.0f, 3.0f, -3.0f), glm::vec3(0.0f, 1.0f, 0.0f), -90.0f, 0.0f, 20.0f, 0.5f);
	brickTexture = Texture("textures/brick.png");
	brickTexture.LoadTextureA();
	marbleTexture  = Texture("textures/marble.jpg");
	marbleTexture.LoadTexture();
	plainTexture = Texture("textures/plain.png");
	plainTexture.LoadTextureA();


	shinyMaterial = Material(4.0f, 256);
	dullMaterial = Material(0.3f, 4);

    plainTexture = Texture("textures/plain.png");
	plainTexture.LoadTextureA();

	mainLight = DirectionalLight(1242, 1242,
								1.0f, 1.0f, 1.0f, 
								0.6f, 0.3f,
								0.0f, -15.0f, -10.0f);

	fstream fin; 
    // Open an existing file 
    fin.open(fileName, ios::in); 
	string line;
	int count = 0;
	Model* car1 = new Model(0, 0, 0);
	car1->LoadModel("assets/car/car.obj");
	Model* car2 = new Model(0, 0, 0);
	car2->LoadModel("assets/SUV/SUV.obj");
	Model* person = new Model(0, 0, 0);
	person->LoadModel("assets/person/person.obj");
	Model* building = new Model(0, 0, 0);
	building->LoadModel("assets/building/building.obj");
	Model* sidewalk = new Model(0, 0, 0);
	sidewalk->LoadModel("assets/side/sidewalk.obj");
	Model* vegetation = new Model(0, 0, 0);
	vegetation->LoadModel("assets/tree2/Tree.obj");
	while(getline(fin, line))
	{
		if (count == 0)
		{
			count++;
			continue;
		}

		 
        stringstream s(line); 
		string word;
		vector<string> row;
		while(s.good())
		{
			string substr;
			getline(s, substr, ' ');
			row.push_back(substr);
		}
        
		ModelInputParams params = ModelInputParams(row[0], 
												   stof(row[1]), stof(row[2]), stof(row[3]),
												   stof(row[4]), stof(row[5]), stof(row[6]),
												   stof(row[7]), stof(row[8]), stof(row[9]));

		Model* model;
		if(row[0] == "car1")
			model = car1;
		if(row[0] == "car")
			model = car2;
		if(row[0] == "person")
			model = person;
		if(row[0] == "building")
			model = building;
		if(row[0] == "vegetation")
			model = vegetation;
		if(row[0] == "sidewalk")
			model = sidewalk;

		model->xPos = params.x;
		model->yPos = params.y;
		model->depth = params.z;
		model->colour = glm::vec3(1.0);
		model->rotX = params.xrot;
		model->rotY = params.yrot;
		model->rotZ = params.zrot;	
		model->scaleX = params.xscale;
		model->scaleY = params.yscale;
		model->scaleZ = params.zscale; 

		modelList.push_back(*model);
       
	}

  	projection = glm::perspective(toRadians * 70.0f, (GLfloat)mainWindow.getBufferWidth() / mainWindow.getBufferHeight(), 0.1f, 850.0f);
	
}
