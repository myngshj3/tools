Imports System.io.Text
Imports System.data

'---- This is test class for parser
Partial Public Class Test

    Public Sub Page_Load()
        Dim str As String = "Hello 'World'" 'Comment Deleting Feature
        str.dup()
        Method()
    End Sub

    Public Function Method()
        Dim CS As DataServer
        CS.Encode()
        CS.Insert()
    End Function

    Public Function Concrete()
        Dim str As String
        str.replace("Hello", "World")
    End Function

    Public Sub CallStoredProcedure()
        Dim DC As DataController = New DataController()
        DC.StoredProcedure = "Sel_Trn_LRecipINfo_SouNo_Excel"

    End Sub

End Class
