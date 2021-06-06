#include "python.h" 

static PyObject*
GetLuckyNumber(PyObject* self, PyObject* args)
{
    int inum, iage;
    const char* istr;

    if (!PyArg_ParseTuple(args, "isi", &inum, &istr, &iage))
        return NULL;

    FILE* fp = NULL;
    fopen_s(&fp, "PredictSet.txt", "r");
    if (fp == NULL) return 0;

    int top1, top2, top3;
    int age, num;
    char sex;
    fscanf_s(fp, "%d %d %d %d %d %c \n", &top1, &top2, &top3, &age, &num, &sex);
    fclose(fp);
    return Py_BuildValue("iiC", age, num, sex);
    /*int numval=0, ageval=0, sexval=0;
    while (!feof(fp)) {
        int top1, top2, top3;
        int age, num;
        char* sex = NULL;

        fscanf(fp, "%d %d %d %d %d %s \n", &top1, &top2, &top3, &age, &num, sex);

        if (inum == num) {
            numval += top1 + top2 + top3;
        }
        if (iage == age) {
            ageval += top1 + top2 + top3;
        }
        if (!strcmp(istr, sex)) {
            sexval += top1 + top2 + top3;
        }
        return Py_BuildValue("[i,i,s]", age, num, sex);
    }
    fclose(fp);
    
    return Py_BuildValue("[i,i,i]", numval, ageval, sexval);*/
}

static PyMethodDef GetLuckyMethods[] = {
    {"GetLuckyNumber", GetLuckyNumber, METH_VARARGS,
    "Get lucky number of next racing"},
    {NULL, NULL, 0, NULL}    //배열의 끝을 나타낸다.
};


static struct PyModuleDef GetLuckymodule = {
    PyModuleDef_HEAD_INIT,
    "GetLucky",            // 모듈 이름
    "For Predict Horse-Racing using RandomForest", // 모듈 설명을 적는 부분, 모듈의 __doc__에 저장됩니다.
    -1,GetLuckyMethods
};

PyMODINIT_FUNC
PyInit_GetLucky(void)
{
    return PyModule_Create(&GetLuckymodule);
}
