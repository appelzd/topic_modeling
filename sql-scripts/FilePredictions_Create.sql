/****** Object:  Table [dbo].[PyTest]    Script Date: 11/11/2019 8:20:00 PM ******/
DROP TABLE [dbo].[FilePredictions]
GO

/****** Object:  Table [dbo].[PyTest]    Script Date: 11/11/2019 8:20:00 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[FilePredictions](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[FileName] [varchar](max) NOT NULL,
	[TopicId] [int] NOT NULL,
	[Likelyhood] [decimal](18, 4) NOT NULL,
 CONSTRAINT [PK_FilePredictions] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


