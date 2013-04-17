class ApplicationController < ActionController::Base
	protect_from_forgery


	def runit
		@code = params[:token]
		tmp_file = "#{Rails.root}/public/files/tmp.swim"
		id = 0
		while File.exists?(tmp_file) do
			tmp_file = "#{Rails.root}/public/files/tmp-#{id}.swim"        
			id += 1
		end
		File.open(tmp_file, 'wb') do |f|
			f.write  @code
		end
		@retval = `#{Rails.root}/public/bin/swim_osx #{tmp_file}`
		render :text =>  @retval
		logger.info @retval.to_json
		
	end

end